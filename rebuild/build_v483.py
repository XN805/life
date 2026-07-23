from pathlib import Path

parts = [Path(f"rebuild/base_{index:03d}.part").read_text(encoding="utf-8") for index in range(1, 7)]
base = "".join(parts)

editor_start_marker = '<div id="momentEditorParking"'
editor_end_marker = '<div class="add-moment-zone"'
if editor_start_marker not in base or editor_end_marker not in base:
    raise SystemExit("editor replacement markers missing")
editor_start = base.index(editor_start_marker)
editor_end = base.index(editor_end_marker, editor_start)
editor = Path("rebuild/editor_v483.htmlfrag").read_text(encoding="utf-8")
base = base[:editor_start] + editor + base[editor_end:]

if "<script>" not in base:
    raise SystemExit("original script marker missing")
base = base.rsplit("<script>", 1)[0]
patch = Path("rebuild/v483_patch.htmlfrag").read_text(encoding="utf-8")
old_render = "function renderMoments(){const list=orderedMoments();$('momentList').innerHTML=list.map((m,i)=>momentCard(m,i)).join('');"
new_render = "function renderMoments(){const editor=$('momentEditor'),parking=$('momentEditorParking');if(editor&&parking&&editor.parentElement!==parking)parking.appendChild(editor);const list=orderedMoments();$('momentList').innerHTML=list.map((m,i)=>momentCard(m,i)).join('');"
old_mount = "const active=activeMoment(),host=q(`[data-editor-host=\"${active.id}\"]`);if(host)host.appendChild($('momentEditor'))}"
new_mount = "const active=activeMoment(),host=q(`[data-editor-host=\"${active.id}\"]`);if(host&&editor)host.appendChild(editor)}"
if old_render not in patch or old_mount not in patch:
    raise SystemExit("renderMoments patch markers missing")
patch = patch.replace(old_render, new_render, 1).replace(old_mount, new_mount, 1)

out = base + patch
out = out.replace("AI朋友圈 v4.8.2", "AI朋友圈 v4.8.3")
out = out.replace("，最多10个。", "。")
out = out.replace("当前 1 个任务，最多 10 个", "")
out = out.replace("共用发布员工和可见客户，最多10个任务", "共用发布员工和可见客户")

output_dir = Path("dist")
output_dir.mkdir(exist_ok=True)
output = output_dir / "ai_moments_v4_8_3_reviewed.html"
output.write_text(out, encoding="utf-8")
print(f"built {output} ({len(out):,} characters)")
