; ;;; Lab08: Scheme

; (define (over-or-under a b)
;   (if (= a b) 0 (if (< a b) -1 1))
;   )


; (define (make-adder n)
;   (define (adder x) (+ x n)
;     )
;   adder
;   )



; (define (composed f g)
;   (lambda (x) (f (g x))
;     )
;   )


; (define (remainder a b)
;   (- a (* b (quotient a b))))

; (define (gcd a b)
;   (if (= b 0) a (gcd b (remainder a b))
;     )
;   )


; (define lst
;   (cons (cons 1 nil) (cons 2 (cons (cons 3 (cons 4 nil)) (cons 5 nil)))
;   )
; )


; (define (ordered s)
;   (if (null? s) #t
;     (if (null? (cdr s)) #t
;       (if (> (car s) (car (cdr s))) #f 
;         (ordered (cdr s))
;       )
;     )
;   )
; )

