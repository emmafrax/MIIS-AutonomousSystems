(define (domain sokoban) 
    (:requirements :typing) 
    (:types x y) 
    (:predicates (at ?x - x ?y - y)(iswall ?x - x ?y - y)(hasbox ?x - x ?y - y)(hastp)(incx ?x1 ?x2 - x)(incy ?y1 ?y2 - y)(decx ?x1 ?x2 - x )(decy ?y1 ?y2 - y )(samex ?x1 ?x2 - x)(samey ?y1 ?y2)) 
    (:action moveup
    :parameters (?xfrom ?xto - x ?yfrom ?yto - y)
    :precondition (and (at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(incy ?yfrom ?yto)(samex ?xfrom ?xto)(not(hasbox ?xto ?yto)))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))))
    (:action movedown
    :parameters (?xfrom ?xto - x ?yfrom ?yto - y)
    :precondition (and (at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(decy ?yfrom ?yto)(samex ?xfrom ?xto)(not(hasbox ?xto ?yto)))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))))
    (:action moveright
    :parameters (?xfrom ?xto - x ?yfrom ?yto - y)
    :precondition (and (at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(incx ?xfrom ?xto)(samey ?yfrom ?yto)(not(hasbox ?xto ?yto)))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))))
    (:action moveleft
    :parameters (?xfrom ?xto - x ?yfrom ?yto - y)
    :precondition (and (at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(decx ?xfrom ?xto)(samey ?yfrom ?yto)(not(hasbox ?xto ?yto)))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))))
    (:action moveboxup
    :parameters (?xfrom ?xto ?xboxto - x ?yfrom ?yto ?yboxto - y)
    :precondition (and (not(hasbox ?xboxto ?yboxto))(at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(not(iswall ?xboxto ?yboxto))(incy ?yfrom ?yto)(incy ?yto ?yboxto)(samex ?xfrom ?xto)(samex ?xto ?xboxto)(hasbox ?xto ?yto))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))(hasbox ?xboxto ?yboxto)(not (hasbox ?xto ?yto))))    
  (:action moveboxdown
    :parameters (?xfrom ?xto ?xboxto - x ?yfrom ?yto ?yboxto - y)
    :precondition (and (not(hasbox ?xboxto ?yboxto))(at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(not(iswall ?xboxto ?yboxto))(decy ?yfrom ?yto)(decy ?yto ?yboxto)(samex ?xfrom ?xto)(samex ?xto ?xboxto)(hasbox ?xto ?yto))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))(hasbox ?xboxto ?yboxto)(not (hasbox ?xto ?yto))))    
  (:action moveboxright
    :parameters (?xfrom ?xto ?xboxto - x ?yfrom ?yto ?yboxto - y)
    :precondition (and (not(hasbox ?xboxto ?yboxto))(at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(not(iswall ?xboxto ?yboxto))(incx ?xfrom ?xto)(incx ?xto ?xboxto)(samey ?yfrom ?yto)(samey ?yto ?yboxto)(hasbox ?xto ?yto))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))(hasbox ?xboxto ?yboxto)(not (hasbox ?xto ?yto))))    
  (:action moveboxleft
    :parameters (?xfrom ?xto ?xboxto - x ?yfrom ?yto ?yboxto - y)
    :precondition (and (not(hasbox ?xboxto ?yboxto))(at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(not(iswall ?xboxto ?yboxto))(decx ?xfrom ?xto)(decx ?xto ?xboxto)(samey ?yfrom ?yto)(samey ?yto ?yboxto)(hasbox ?xto ?yto))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))(hasbox ?xboxto ?yboxto)(not (hasbox ?xto ?yto))))    
  (:action teleport
    :parameters (?xfrom ?xto - x ?yfrom ?yto - y)
    :precondition (and (at ?xfrom ?yfrom)(not(iswall ?xto ?yto))(not(hasbox ?xto ?yto))(not(hastp)))
    :effect (and (at ?xto ?yto)(not (at ?xfrom ?yfrom))(hastp)))    
       )

