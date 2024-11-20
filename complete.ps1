$scriptblock = {
	param(
		$wordToComplete,
		$commandAst,
		$cursorPosition
	)

	py -m pwsh_git --complete $commandAst.ToString() | ForEach-Object {
		[System.Management.Automation.CompletionResult]::new(
			$_,               # completionText
			$_,               # listItemText
			'ParameterValue', # resultType
			$_                # toolTip
		)
	}
}

Register-ArgumentCompleter -Native -CommandName git -ScriptBlock $scriptblock
