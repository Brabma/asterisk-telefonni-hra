$ErrorActionPreference = 'Stop'
$data = [Console]::In.ReadToEnd() | ConvertFrom-Json

Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.SpeechSynthesis.SpeechSynthesisStream, Windows.Media.SpeechSynthesis, ContentType = WindowsRuntime] | Out-Null
[Windows.Storage.Streams.DataReader, Windows.Storage.Streams, ContentType = WindowsRuntime] | Out-Null

function Wait-WinRtOperation {
    param($Operation, [Type]$ResultType)
    $method = [System.WindowsRuntimeSystemExtensions].GetMethods() |
        Where-Object {
            $_.Name -eq 'AsTask' -and
            $_.IsGenericMethodDefinition -and
            $_.GetParameters().Count -eq 1 -and
            $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
        } |
        Select-Object -First 1
    $task = $method.MakeGenericMethod($ResultType).Invoke($null, @($Operation))
    $task.Wait()
    return $task.Result
}

$synth = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::new()
$stream = $null
$reader = $null
try {
    if ($data.voice) {
        $requested = [string]$data.voice
        $match = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices |
            Where-Object { $requested -eq $_.DisplayName -or $requested.StartsWith($_.DisplayName) -or $requested -eq $_.Id } |
            Select-Object -First 1
        if ($match) { $synth.Voice = $match }
    }

    $escaped = [Security.SecurityElement]::Escape([string]$data.text)
    $percent = [Math]::Max(-40, [Math]::Min(40, [int]$data.rate * 8))
    $rate = if ($percent -ge 0) { "+$percent%" } else { "$percent%" }
    $pitchPercent = [Math]::Max(-50, [Math]::Min(80, [int](([double]$data.pitch - 1.0) * 100)))
    $pitch = if ($pitchPercent -ge 0) { "+$pitchPercent%" } else { "$pitchPercent%" }
    $language = if ($synth.Voice.Language) { $synth.Voice.Language } else { 'cs-CZ' }
    $ssml = "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='$language'><prosody rate='$rate' pitch='$pitch'>$escaped</prosody></speak>"

    $operation = $synth.SynthesizeSsmlToStreamAsync($ssml)
    $stream = Wait-WinRtOperation $operation ([Windows.Media.SpeechSynthesis.SpeechSynthesisStream])
    $reader = [Windows.Storage.Streams.DataReader]::new($stream)
    [void](Wait-WinRtOperation ($reader.LoadAsync([uint32]$stream.Size)) ([uint32]))
    $bytes = New-Object byte[] ([int]$stream.Size)
    $reader.ReadBytes($bytes)
    [IO.File]::WriteAllBytes([string]$data.path, $bytes)
} finally {
    if ($reader) { $reader.Dispose() }
    if ($stream) { $stream.Dispose() }
    $synth.Dispose()
}
