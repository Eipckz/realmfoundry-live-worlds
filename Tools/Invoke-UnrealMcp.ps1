[CmdletBinding(DefaultParameterSetName = 'List')]
param(
    [Parameter(ParameterSetName = 'Describe', Mandatory)]
    [string]$DescribeToolset,

    [Parameter(ParameterSetName = 'Call', Mandatory)]
    [string]$Toolset,

    [Parameter(ParameterSetName = 'Call', Mandatory)]
    [string]$Tool,

    [Parameter(ParameterSetName = 'Call')]
    [string]$ArgumentsJson = '{}',

    [Parameter(ParameterSetName = 'Batch', Mandatory)]
    [string]$BatchJson,

    [string]$Url = 'http://127.0.0.1:8000/mcp'
)

$ErrorActionPreference = 'Stop'
$protocolVersion = '2025-11-25'
$headers = @{ Accept = 'application/json, text/event-stream' }

function Invoke-McpRequest {
    param(
        [Parameter(Mandatory)] [hashtable]$Body,
        [string]$SessionId
    )

    $requestHeaders = $headers.Clone()
    if ($SessionId) {
        $requestHeaders['Mcp-Session-Id'] = $SessionId
    }

    Invoke-WebRequest `
        -Uri $Url `
        -Method Post `
        -Headers $requestHeaders `
        -ContentType 'application/json' `
        -Body ($Body | ConvertTo-Json -Depth 100 -Compress) `
        -UseBasicParsing
}

$initialize = Invoke-McpRequest -Body @{
    jsonrpc = '2.0'
    id = 1
    method = 'initialize'
    params = @{
        protocolVersion = $protocolVersion
        capabilities = @{}
        clientInfo = @{ name = 'realmfoundry-project-client'; version = '1.0' }
    }
}

$sessionId = [string]$initialize.Headers['Mcp-Session-Id']
if (-not $sessionId) {
    throw 'Unreal MCP initialize response did not include Mcp-Session-Id.'
}

$initializedJson = @{ jsonrpc = '2.0'; method = 'notifications/initialized'; params = @{} } |
    ConvertTo-Json -Depth 10 -Compress
& curl.exe -sS --max-time 2 -X POST $Url `
    -H 'Content-Type: application/json' `
    -H 'Accept: application/json, text/event-stream' `
    -H "Mcp-Session-Id: $sessionId" `
    --data $initializedJson | Out-Null

switch ($PSCmdlet.ParameterSetName) {
    'Describe' {
        $params = @{ name = 'describe_toolset'; arguments = @{ toolset_name = $DescribeToolset } }
    }
    'Call' {
        $arguments = $ArgumentsJson | ConvertFrom-Json -AsHashtable
        $params = @{
            name = 'call_tool'
            arguments = @{
                toolset_name = $Toolset
                tool_name = $Tool
                arguments = $arguments
            }
        }
    }
    'Batch' {
        $batch = @($BatchJson | ConvertFrom-Json -AsHashtable)
        $responses = @()
        $requestId = 2
        foreach ($item in $batch) {
            $batchParams = @{
                name = 'call_tool'
                arguments = @{
                    toolset_name = [string]$item.toolset
                    tool_name = [string]$item.tool
                    arguments = if ($item.arguments) { $item.arguments } else { @{} }
                }
            }
            $batchResponse = Invoke-McpRequest -SessionId $sessionId -Body @{
                jsonrpc = '2.0'
                id = $requestId
                method = 'tools/call'
                params = $batchParams
            }
            $responses += ($batchResponse.Content | ConvertFrom-Json -Depth 100)
            $requestId++
        }
        $responses | ConvertTo-Json -Depth 100
        return
    }
    default {
        $params = @{ name = 'list_toolsets'; arguments = @{} }
    }
}

$response = Invoke-McpRequest -SessionId $sessionId -Body @{
    jsonrpc = '2.0'
    id = 2
    method = 'tools/call'
    params = $params
}

$response.Content
