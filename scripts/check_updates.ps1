# TODO(milestone 3): count pending Windows updates and print JSON for the agent.
# Hint: $s = New-Object -ComObject Microsoft.Update.Session
#       $r = $s.CreateUpdateSearcher().Search("IsInstalled=0 and Type='Software'")
#       @{ count = $r.Updates.Count } | ConvertTo-Json
