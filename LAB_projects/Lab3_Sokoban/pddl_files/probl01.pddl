(define (problem monkeyinst)
    (:domain mon-ban)
    (:objects loc1 loc2 loc3 loc4 loc5 loc6 loc7 loc8 loc9 - loc b1 b2 - banana c1 c2 - chair)
    (:init (at-monkey loc1)(at-ch c1 loc9)(at-ch c2 loc5)(at b1 loc6)(at b2 loc8))
    (:goal (and (bananaEaten b1)(bananaEaten b2)))
)


