(define (domain mon-ban) 
    (:requirements :typing) 
    (:types loc banana chair) 
    (:predicates (at-monkey ?l - loc)(at-ch ?c - chair ?l - loc)(at ?b - banana ?l - loc)(bananaEaten ?b - banana)(ChairCarried ?c)) 
    (:action move
    :parameters (?from ?to - loc)
    :precondition (at-monkey ?from)
    :effect (and (at-monkey ?to) (not (at-monkey ?from))))
    (:action pickchair
    :parameters (?obj - banana ?loc - loc ?ch - chair)
    :precondition (and (not(at ?obj ?loc))(at-ch ?ch ?loc)(at-monkey ?loc)(not(ChairCarried ?ch)))
    :effect (and (ChairCarried ?ch)(not(at-ch ?ch ?loc))))
    (:action leavechair
    :parameters (?obj - banana ?loc - loc ?ch - chair)
    :precondition (and (at ?obj ?loc)(at-monkey ?loc)(ChairCarried ?ch))
    :effect (and (not(ChairCarried ?ch))(at-ch ?ch ?loc)))
    (:action grabeat
    :parameters (?obj - banana ?loc - loc ?ch - chair)
    :precondition (and (at-ch ?ch ?loc)(at ?obj ?loc)(at-monkey ?loc)(not(ChairCarried ?ch))(not(bananaEaten ?obj)))
    :effect (and (bananaEaten ?obj)(not (at ?obj ?loc))))
    )

