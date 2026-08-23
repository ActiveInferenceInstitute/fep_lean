# Packaged catalogue data

`topics.yaml` is the wheel-readable, byte-identical projection of the checkout
`config/topics.yaml`. It is generated from metadata, theorem maturity, the
validated novelty ledger, and canonical family-owned Lean bodies; never edit it
by hand.

`FEPTopicCatalogue.default()` reads this resource through `importlib.resources`
so the installed package does not depend on the source checkout.
