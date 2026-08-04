param(
    [Parameter(Mandatory)]
    [string]$InputText,

    [string]$Model = "onion-model-a"
)

$promptPath = Join-Path $PSScriptRoot "prompts/mnd_n_signal_prompt.txt"
$systemPrompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8
$prompt = "$systemPrompt`n`n사용자 발화:`n$InputText"

$timer = [System.Diagnostics.Stopwatch]::StartNew()

try {
    $output = (
        & ollama run $Model $prompt `
            --format json `
            --think=false `
            --hidethinking `
            --nowordwrap `
            --keepalive 5m 2>$null
    ) -join ""
} finally {
    $timer.Stop()
}

[PSCustomObject]@{
    input = $InputText
    model = $Model
    latency_seconds = [Math]::Round($timer.Elapsed.TotalSeconds, 2)
    output = $output.Trim()
}
