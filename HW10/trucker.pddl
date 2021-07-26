(define (domain trucker)
   (:predicates (location ?l)
		(package ?p)
		(truck ?t)
		(at-loc ?l)
		(at ?p ?l)
		(free ?t)
		(carry ?p ?t))

   (:action move
       :parameters (?from ?to)
       :precondition (and (location ?from) (location ?to) (at-loc ?from))
       :effect (and (at-loc ?to)
		     (not (at-loc ?from))))

   (:action pick
       :parameters (?pckg ?loc ?t)
       :precondition  (and (package ?pckg) (location ?loc) (truck ?t)
			    (at ?pckg ?loc) (at-loc ?loc) (free ?t))
       :effect (and (carry ?pckg ?t)
		    (not (at ?pckg ?loc))
		    (not (free ?t))))

   (:action drop
       :parameters (?pckg ?loc ?t)
       :precondition (and (package ?pckg) (location ?loc) (truck ?t)
			    (carry ?pckg ?t) (at-loc ?loc))
       :effect (and (at ?pckg ?loc)
		    (free ?t)
		    (not (carry ?pckg ?t)))))

