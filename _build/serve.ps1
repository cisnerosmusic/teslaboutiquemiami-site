# Minimal static file server for local preview (no Node/Python required).
param([int]$Port = 8099, [string]$Root = "E:\our music\COWORK\teslaboutiquemiami-site")

$mime = @{
  ".html"="text/html; charset=utf-8"; ".css"="text/css; charset=utf-8";
  ".js"="application/javascript"; ".png"="image/png"; ".jpg"="image/jpeg";
  ".jpeg"="image/jpeg"; ".webp"="image/webp"; ".avif"="image/avif";
  ".svg"="image/svg+xml"; ".ico"="image/x-icon"; ".json"="application/json";
  ".woff"="font/woff"; ".woff2"="font/woff2"; ".xml"="application/xml"; ".txt"="text/plain"
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add("http://localhost:$Port/")
$listener.Start()
Write-Host "Serving $Root at http://localhost:$Port/"

while ($listener.IsListening) {
  $ctx = $listener.GetContext()
  $req = $ctx.Request; $res = $ctx.Response
  try {
    $rel = [System.Uri]::UnescapeDataString($req.Url.AbsolutePath.TrimStart('/'))
    if ($rel -eq "") { $rel = "index.html" }
    $path = Join-Path $Root $rel
    if ((Test-Path $path -PathType Container)) { $path = Join-Path $path "index.html" }
    if (Test-Path $path -PathType Leaf) {
      $ext = [System.IO.Path]::GetExtension($path).ToLower()
      $ct = $mime[$ext]; if (-not $ct) { $ct = "application/octet-stream" }
      $res.ContentType = $ct
      $res.Headers.Add("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
      $res.Headers.Add("Pragma", "no-cache")
      $bytes = [System.IO.File]::ReadAllBytes($path)
      $res.ContentLength64 = $bytes.Length
      $res.OutputStream.Write($bytes, 0, $bytes.Length)
    } else {
      $res.StatusCode = 404
      $msg = [System.Text.Encoding]::UTF8.GetBytes("404 Not Found: $rel")
      $res.OutputStream.Write($msg, 0, $msg.Length)
    }
  } catch {
    $res.StatusCode = 500
  } finally {
    $res.OutputStream.Close()
  }
}
