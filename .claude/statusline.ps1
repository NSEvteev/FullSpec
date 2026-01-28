# StatusLine script for Claude Code
# Reads JSON from stdin and outputs formatted status line

$input_json = $input | Out-String
if ($input_json) {
    $data = $input_json | ConvertFrom-Json

    $model = $data.model.id
    $remaining = [math]::Round($data.context_window.remaining_percentage, 0)
    $size = [math]::Round($data.context_window.context_window_size / 1000, 0)

    Write-Host "$model | ctx: ${remaining}% | ${size}k"
}
