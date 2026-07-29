param(
    [Parameter(Mandatory)]
    [string]$InputText,

    [string]$Model = "qwen3:1.7b",

    [string]$ApiUrl = "http://localhost:11434/v1/chat/completions"
)

$promptPath = Join-Path $PSScriptRoot "prompts/mnd_n_signal_prompt.txt"
$systemPrompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8

$body = @{
    model = $Model
    temperature = 0
    max_tokens = 200
    stream = $false
    response_format = @{
        type = "json_object"
    }
    messages = @(
        @{
            role = "system"
            content = $systemPrompt
        },
        @{
            role = "user"
            content = $InputText
        }
    )
} | ConvertTo-Json -Depth 10

$timer = [System.Diagnostics.Stopwatch]::StartNew()

try {
    $response = Invoke-RestMethod `
        -Uri $ApiUrl `
        -Method Post `
        -ContentType "application/json; charset=utf-8" `
        -Body $body
} finally {
    $timer.Stop()
}

[PSCustomObject]@{
    input = $InputText
    model = $Model
    latency_seconds = [Math]::Round($timer.Elapsed.TotalSeconds, 2)
    output = $response.choices[0].message.content
}
