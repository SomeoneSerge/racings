# Racings base package


## Intro

This is an all-in-one nasty package
that is going to contain
the relational (I prefer "1st order logic" actually) model,
the validation rules (corresponding to higher-order constraints),
the database details (SQLAlchemy (hereafter SQLA) models)... you name it.

## Nastyness

A bit of clarification on the "nastyness" of this solution.
I don't mind these things residing in same package
but I do mind these things being inseparable.
In the existing stacks it is rather hard to decompose an application
into independent, reusable and pluggable modules.
Most of the frameworks that claim to provide such an opportunity
and means to it. Well that's a big huge lie.
They always create some unneeded dependencies
in most inappropriate ways and directions.
Take a look at SQLA for example:
in order to describe an entity within your model
you have to pass the global `metadata` object instance
to the entity definition code.
This is fundamentally ill.
Imagine you're writing some extension for your application.
An extension that does not really affect the rest of the models
but merely... Well, extends it.
Suppose also that the problem this extension solves
is somewhat typical and arises repeatedly.
As a sane person You'd try to write this extension
as a pluggable module that you could simply mention in the config
of your application and have it up and running.

In SQLA that is not well supported.
You could write factory methods in your new package
that'd take as an argument and put new entities into the `metadata`.
You'd then setup your application to iterate
over all such pluggable modules and find&apply all of such methods.
This procedure needs to be generalized and implemented in some library.
One could object and mention Django or Spring.
I'll just say that these are even nastier solutions
and one day I might elaborate on this.
This document is not a place for this topic.

## Justifications for SQLA models-related decisions

The SQLA is used merely as an abstraction for SQL and RDBMSs.
The `domain.py` contains relational models described in SQLA.
It was a goal to describe them in the normalized form.
That is in the form of first-order logic propositions.
The model contains a lot of tables which could've been stripped out.
The reason they exist for is that of modeling integrity constraints
(which is the main purpose of relational model which is always mentioned
by devs in the field and which is **always** misused;
devs without math background are dumb and naive,
so they would for example spoil every single integrity guarantee
by issuing multiple sequential `select` queries;
they think it is enough that they use transactions for data modification;
but when they use some stupid framework to query
"the lists of $y$s for each $x$"
they end up screwing the integrity and performance;
that is because RDBMSs and frameworks are also being "developed"
by ignorant morons).
Hence we've got an empty `Manufacturer` entity
whose purpose is to constrain the manufacturers
of say cars to actually be manufacturers
and not just some random people.
