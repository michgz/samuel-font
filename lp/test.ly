\version "2.20.0"
\paper {
  #(define fonts
    (set-global-fonts
     #:music "samuel"
     #:brace "emmentaler"
   ))
}
{
 % \override Staff.TimeSignature.font-name=#"samuel-14"
 % \override Staff.TimeSignature.font-size=#5
 % \override Staff.Clef.font-name=#"samuel-14"
 % \override Staff.Clef.font-family=#roman
 % \override Staff.Clef.font-size=#15
 % \override Staff.Clef.glyph-name=#"four"
 \time 3/4
  c' e' g' e'
}
