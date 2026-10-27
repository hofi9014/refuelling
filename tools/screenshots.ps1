# Store screenshots (1080x1920) of the demo data, in a throwaway headless Chrome profile.
# Needs the local server running: python -m http.server 8765 --directory docs
# Headless Chrome won't go below ~500 px wide, so the page is rendered at 1080x1920 with the app's own zoom at 3x (= a 360x640 phone).
param([string]$Base = "http://localhost:8765/", [string[]]$Langs = @("pl", "en"))

$chrome = @("C:\Program Files\Google\Chrome\Application\chrome.exe",
            "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe") | Where-Object { Test-Path $_ } | Select-Object -First 1
$root = Split-Path $PSScriptRoot -Parent
$profileDir = Join-Path $env:TEMP "refuelling-shots-profile"
$shots = [ordered]@{
    "1-dashboard" = "tab=dashboard"
    "2-trends"    = "tab=dashboard&at=trends"
    "3-timeline"  = "tab=fuel"
    "4-fillup"    = "tab=dashboard&open=fuel"
    "5-reports"   = "tab=reports"
    "6-costs"     = "tab=costs"
}
foreach ($lang in $Langs) {
    $out = Join-Path $root "store\screenshots\$lang"
    New-Item -ItemType Directory -Force $out | Out-Null
    foreach ($name in $shots.Keys) {
        $url = "$($Base)?demo&z=3&lang=$lang&$($shots[$name])"
        Start-Process $chrome -Wait -WindowStyle Hidden -ArgumentList @("--headless=new", "--disable-gpu", "--hide-scrollbars",
            "--user-data-dir=`"$profileDir`"", "--window-size=1080,1920", "--virtual-time-budget=5000",
            "--blink-settings=preferredColorScheme=1", "--screenshot=`"$out\$name.png`"", "`"$url`"")
        Write-Output "$lang/$name.png"
    }
}
Remove-Item -Recurse -Force $profileDir -ErrorAction SilentlyContinue
