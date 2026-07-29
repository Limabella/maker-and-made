param(
    [Parameter(Mandatory)]
    [string]$InputText,

    [string]$Model = "qwen3:1.7b",

    [string]$ApiUrl = "http://localhost:11434/api/chat"
)

$promptPath = Join-Path $PSScriptRoot "prompts/mnd_n_signal_prompt.txt"
$systemPrompt = Get-Content -LiteralPath $promptPath -Raw -Encoding UTF8

$body = @{
    model = $Model
    stream = $false
    think = $false
    format = "json"
    keep_alive = "5m"
    options = @{
        temperature = 0
        num_predict = 200
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
$httpClient = [System.Net.Http.HttpClient]::new()
$httpClient.Timeout = [TimeSpan]::FromSeconds(60)
$httpContent = [System.Net.Http.StringContent]::new(
    $body,
    [System.Text.Encoding]::UTF8,
    "application/json"
)

try {
    $httpResponse = $httpClient.PostAsync($ApiUrl, $httpContent).GetAwaiter().GetResult()
    $responseText = $httpResponse.Content.ReadAsStringAsync().GetAwaiter().GetResult()
    if (-not $httpResponse.IsSuccessStatusCode) {
        throw "Ollama returned HTTP $([int]$httpResponse.StatusCode): $responseText"
    }
    $response = $responseText | ConvertFrom-Json
} finally {
    $httpContent.Dispose()
    $httpClient.Dispose()
    $timer.Stop()
}

[PSCustomObject]@{
    input = $InputText
    model = $Model
    latency_seconds = [Math]::Round($timer.Elapsed.TotalSeconds, 2)
    load_seconds = [Math]::Round($response.load_duration / 1000000000, 2)
    prompt_tokens = $response.prompt_eval_count
    output_tokens = $response.eval_count
    output = $response.message.content
}
