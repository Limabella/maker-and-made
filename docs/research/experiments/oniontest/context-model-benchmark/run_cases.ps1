param(
    [string]$Model = "onion-model-a",
    [string]$OutputPath = ""
)

$casesPath = Join-Path $PSScriptRoot "cases.jsonl"
$manualTestPath = Join-Path $PSScriptRoot "manual_test.ps1"
$cases = Get-Content -LiteralPath $casesPath -Encoding UTF8 |
    ForEach-Object { $_ | ConvertFrom-Json }

$results = foreach ($case in $cases) {
    Write-Host "Running $($case.case_id) with $Model..."
    $result = & $manualTestPath -InputText $case.input -Model $Model

    [PSCustomObject]@{
        case_id = $case.case_id
        model = $Model
        input = $case.input
        gold = $case.gold
        latency_seconds = $result.latency_seconds
        output = $result.output | ConvertFrom-Json
    }
}

$json = $results | ConvertTo-Json -Depth 10
if ($OutputPath) {
    $parent = Split-Path -Parent $OutputPath
    if ($parent) {
        New-Item -ItemType Directory -Force -Path $parent | Out-Null
    }
    Set-Content -LiteralPath $OutputPath -Value $json -Encoding UTF8
    Write-Host "Saved: $OutputPath"
}

$json
