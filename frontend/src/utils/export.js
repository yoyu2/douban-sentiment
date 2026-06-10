/**
 * 将指定 DOM 元素截图导出为 PNG，打包成 ZIP 下载
 *
 * html2canvas、jszip、file-saver 按需动态加载，
 * 不影响首屏体积
 */
export async function exportReport(movieName, sections) {
  const [{ default: html2canvas }, { default: JSZip }, { saveAs }] =
    await Promise.all([
      import('html2canvas'),
      import('jszip'),
      import('file-saver'),
    ])

  const zip = new JSZip()

  for (const { name, el } of sections) {
    if (!el) continue

    try {
      const canvas = await html2canvas(el, {
        backgroundColor: '#ffffff',
        scale: 2,
        useCORS: true,
        logging: false,
      })

      const blob = await new Promise((resolve) =>
        canvas.toBlob(resolve, 'image/png')
      )

      zip.file(`${name}.png`, blob)
    } catch (err) {
      console.error(`截图失败: ${name}`, err)
    }
  }

  const zipBlob = await zip.generateAsync({ type: 'blob' })
  saveAs(zipBlob, `${movieName}_情感分析报告.zip`)
}
