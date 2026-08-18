param(
    [string]$ToolName,
    [string]$ArgumentsJson = '{}',
    [switch]$ListTools,
    [string]$OutputImagePath,
    [string]$ServerUrl = 'http://127.0.0.1:8000/mcp'
)

$ErrorActionPreference = 'Stop'
$baseHeaders = @{
    Accept = 'application/json, text/event-stream'
    'Content-Type' = 'application/json'
}

function Invoke-RFRequest {
    param(
        [hashtable]$Payload,
        [hashtable]$Headers
    )

    $body = $Payload | ConvertTo-Json -Depth 100 -Compress
    $response = Invoke-WebRequest -Uri $ServerUrl -Method Post -Headers $Headers -Body $body
    [pscustomobject]@{
        Response = $response.Content | ConvertFrom-Json -Depth 100
        Headers = $response.Headers
    }
}

$initialize = Invoke-RFRequest -Headers $baseHeaders -Payload @{
    jsonrpc = '2.0'
    id = 1
    method = 'initialize'
    params = @{
        protocolVersion = '2025-11-25'
        capabilities = @{}
        clientInfo = @{ name = 'RealmFoundry-Codex-Recovery'; version = '2.0' }
    }
}

$sessionId = [string]$initialize.Headers['Mcp-Session-Id']
if ([string]::IsNullOrWhiteSpace($sessionId)) {
    throw 'Unreal MCP initialize response did not include Mcp-Session-Id.'
}

$sessionHeaders = $baseHeaders.Clone()
$sessionHeaders['Mcp-Session-Id'] = $sessionId

$initializedBody = @{
    jsonrpc = '2.0'
    method = 'notifications/initialized'
    params = @{}
} | ConvertTo-Json -Depth 10 -Compress
Invoke-WebRequest -Uri $ServerUrl -Method Post -Headers $sessionHeaders -Body $initializedBody | Out-Null

if ($ListTools) {
    $result = Invoke-RFRequest -Headers $sessionHeaders -Payload @{
        jsonrpc = '2.0'
        id = 2
        method = 'tools/list'
        params = @{}
    }
    $result.Response | ConvertTo-Json -Depth 100
    exit 0
}

if ([string]::IsNullOrWhiteSpace($ToolName)) {
    throw 'Specify -ToolName or -ListTools.'
}

$arguments = $ArgumentsJson | ConvertFrom-Json -AsHashtable -Depth 100
$call = Invoke-RFRequest -Headers $sessionHeaders -Payload @{
    jsonrpc = '2.0'
    id = 3
    method = 'tools/call'
    params = @{
        name = $ToolName
        arguments = $arguments
    }
}

if (-not [string]::IsNullOrWhiteSpace($OutputImagePath)) {
    $textBlock = $call.Response.result.content | Where-Object type -eq 'text' | Select-Object -First 1
    if ($null -eq $textBlock) { throw 'Tool response did not contain a text payload with image data.' }
    $payload = $textBlock.text | ConvertFrom-Json -Depth 100
    $image = $payload.returnValue.image
    if ($null -eq $image -and -not [string]::IsNullOrWhiteSpace([string]$payload.returnValue.data)) {
        $image = $payload.returnValue
    }
    if ([string]::IsNullOrWhiteSpace([string]$image.data)) { throw 'Tool response did not contain returnValue.image.data.' }
    $resolvedParent = Split-Path -Parent $OutputImagePath
    if (-not (Test-Path -LiteralPath $resolvedParent)) { New-Item -ItemType Directory -Path $resolvedParent -Force | Out-Null }
    [System.IO.File]::WriteAllBytes($OutputImagePath, [Convert]::FromBase64String([string]$image.data))
    [pscustomobject]@{
        output_image = $OutputImagePath
        mime_type = $image.mimeType
        camera_location = $payload.returnValue.cameraLocation
        camera_rotation = $payload.returnValue.cameraRotation
        camera_fov = $payload.returnValue.cameraFOV
    } | ConvertTo-Json -Depth 20
    exit 0
}

$call.Response | ConvertTo-Json -Depth 100
