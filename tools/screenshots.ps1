# Store screenshots (1080x1920) of the demo data, in a throwaway headless Chrome profile.
# Needs the local server running: python -m http.server 8765 --directory docs
param([string]$Base = "http://localhost:8765/", [string[]]$Langs = @("pl", "en"))

$chrome = @("C:\Program Files\Google\Chrome\Application\chrome.exe",
            "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
$root = Split-Path $PSScriptRoot -Parent
$profileDir = Join-Path $env:TEMP "refuelling-shots-profile"
$shots = [ordered]@{
    "1-dashboard" = "tab=dashboard"
    "2-trends"    = "tab=dashboard&y=760"
    "3-timeline"  = "tab=fuel"
    "4-fillup"    = "tab=dashboard&open=fuel"
    "5-reports"   = "tab=reports"
    "6-costs"     = "tab=costs"
}
foreach ($lang in $Langs) {
    $out = Join-Path $root "store\screenshots\$lang"
    New-Item -ItemType Directory -Force $out | Out-Null
    foreach ($name in $shots.Keys) {
        $file = Join-Path $out "$name.png"
        $url = "$($Base)?demo&lang=$lang&$($shots[$name])"
        & $chrome --headless=new --disable-gpu --hide-scrollbars --user-data-dir="$profileDir" `
            --window-size=360,640 --force-device-scale-factor=3 --virtual-time-budget=5000 `
            --screenshot="$file" $url 2>$null | Out-Null
        Write-Output "$lang/$name.png"
    }
}
Remove-Item -Recurse -Force $profileDir -ErrorAction SilentlyContinue
