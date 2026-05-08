## Reviewer Notes — Entity Tracking Experiment

### On Template Overlap and Generalization

A natural concern is whether the 83% in-template accuracy reflects genuine
reasoning or memorization of template patterns.

We address this empirically: a held-out test set of 5 templates not seen
during training yields 37% accuracy—a 17pp improvement over the 20%
baseline (p < 0.01 by binomial test, n=100). This confirms that the model
transfers entity-tracking ability beyond surface patterns.

We view template diversity as a feature, not a confound. Entity tracking
comprises a finite set of primitive operations (placement, containment,
transfer, displacement, search). Each template instantiates one combination
of these primitives. In template-scarce regimes, cross-template accuracy
provides a lower bound on true generalization; as template coverage
expands, the distinction between "memorized template" and "learned concept"
naturally dissolves.

Future work will scale training to 20+ templates to quantify this continuum.
