Function MySplitFunction(s)
    Dim temp As String

    Do
      temp = s
      s = Replace(s, "  ", " ") 'remove multiple white spaces
    Loop Until temp = s

    MySplitFunction = Split(Trim(s), " ") 'trim to remove starting/trailing space
End Function

Function guessLinesNum(Row)
    guessLinesNum = 1

    For col = Columns("G").Column To Columns("N").Column
        Text = Cells(Row, col)
        arr = Split(Text, vbNewLine)
        LinesNum = UBound(arr) - LBound(arr) + 1

        If LinesNum > guessLinesNum Then
            guessLinesNum = LinesNum
        End If

    Next col

End Function


Sub Normalize()
'
RowCount = 0

' Remove running headers

Range("A1").Select
' Set Do loop to stop when an empty cell is reached.
Do Until ActiveCell.Text = "Lady Bug" Or RowCount > 10000

   If InStr(ActiveCell.Text, "Boat Name") <> 0 Then
      ' Delete this row
      Rows(ActiveCell.Row).EntireRow.Delete
   Else
     RowCount = RowCount + 1
   End If

   ' Step down 1 row from present location.
   ActiveCell.Offset(1, 0).Select
Loop

' Find merged rows

Range("A1").Select
Do Until ActiveCell.Text = "Lady Bug" Or RowCount > 10000

  Row = ActiveCell.Row

   LinesNum = guessLinesNum(Row)

   If LinesNum > 1 Then

       ' Insert rows below
       Rows(Row + 1).EntireRow.Resize(LinesNum - 1).Insert

        ' Now fill new rows with data
        For col = Columns("G").Column To Columns("N").Column
            Text = Cells(Row, col)
            arr = Split(Text, vbNewLine)
            LinesNum = UBound(arr) - LBound(arr) + 1

            cellWasMerged = False
            If Cells(Row, col).MergeCells Then
                Cells(ActiveCell.Row, col).MergeArea.UnMerge
                cellWasMerged = True
            End If

            For n = 0 To LinesNum - 1
                If cellWasMerged Then
                    Words = MySplitFunction(arr(n))
                    wordsNum = UBound(Words) - LBound(Words) + 1
                    For j = 0 To wordsNum - 1
                        Cells(Row + n, col + j) = Words(j)
                    Next j
                Else
                    Cells(Row + n, col) = arr(n)
                End If
            Next n
        Next col

   End If

   ' Step down 1 row from present location.
   ActiveCell.Offset(1, 0).Select
Loop

  MsgBox ("Done")

  End Sub
