#   racings


## Business problem

For the details skim through https://hackmd.io/s/Bk7YmVOgf


## Technical problem

The task merely conists in data modeling (although I'd rather use the term
"modeling [business processes] using data", see more on't later in [my blog
post](https://newkozlukov.github.io/programming/2018/02/06/data-models/)).
Another thing is that application needs to be implemented as a remotely
accessible multiuser service. Probably WEB will do. The last and the most
intricate task is to make offline work possible. We have to figure out a way to
merge data from several nodes.

Since data is better described and manipulated in relational terms, we'll
explicitly depend on the SQLAlchemy package.
The specification of data will be split across several packages and then
statically composed together in a single package (see `racings.model`).
After that we can easily put some pre-baked interface on top of it (e.g.
`flask-admin`). We will also do that in a separate package (cli tool:
`racings_admin.admin`). In the same manner we'll integrate some REST/HATEOAS
layer to handle the IO (i.e. to automagically implement controllers). E.g. we
could use `eve` (see package `racings_rest`).
With REST end points we can build a frontend using some sodding js framework and
serve it as static content --- a perfect isolation between model layer and
presentation layer.

## Modeling the data before modeling using data

Idealistically, we'd like to achieve the following behavior of our application:
we describe the data in one way or another, then we generate endpoints for them,
and in the end the frontend retrieves plain datastructure and figures out a way
to display to user. We'd want to manually build only a few reusable UI
components and the resulting presentation shall be generated.

Had we managed to do that I'd know we've got a clean, easily maintainable
system. The chances also are the generated presentation would have much better
looks than manually composed one. You know, that's how LaTeX's superior to Word.


## Current implementation

At the moment I've basically described a document-model in terms of SQLA.
The model resides in package `simple_bureaucracy`. It provides definitions of a
"Person", a "DocumentType" and a "Document" instance. These three relations will
do what a RDBMS should be doing. The rationale for this db-within-a-db is to
make the resulting datastructures uniform, allowing them to be process in a
generec manner. This solution is sort of silly as I could've had the same
results out of the box with some Mongo. Nevertheless I've got some model to get
started with and to put `eve` and `flask-admin` on.

In the process I had to solve the problem of SQLA being designed sort of
aggressive in terms of dependencies. The usual workflow is to put to
some shared package's `globals()` either a `metadata` or a `declarative_base()`
instance. Then every package that's meant to extend the model shall statically
import this shared object and use for new definitions.
So of course a normal person would prefer to write factory methods instead of
static coupling. That requires us to establish some conventions.
All these conventions are expressed in the module `modular_sqla.model`

## Further steps

I didn't come to the document-model (or EVA-pattern if you wish) in an instant.
The original intention was to automate generation of the SQLA schema. That'd
look like an app (a domain model) statically composed of several independent
reusable components. Such a tool would also have all the data needed to automate
the presentation generation. It'd be a much more consistent system.
Sounds glorius, doesn't it? Why didn't I take this path since the begining then?
Aye, here's the rub. This schema-generation shall be robust and reproducible and
we'll have to deal with migrations. This need thorough thinking.

So the immediate future looks as follows: I've got some REST I'll begin building
the frontend. Our document model includes some metadata about document's
variables. Specifically, each `DocumentType` and each Variable has a `name`.
These names will be included in the api resource and the frontend can use them
as (CSS) class-names. This allows us not only have a generic view but also
subsitute custom presentations up to having a very specific layout.

At the same time we can begin filling in the data.
Later on I'll probably come up with a reasonable way to compose the data model
and then the whole up with controllers and presentation from a static
configuration of several reusable packages.
If (when) that comes, I'll only have to write database migration script. I'll
still be able to supply the frontend with the very same metadata (variable
names, etc). It's just that this data would be statically composed too.

## Temporarily, Mongo

As I've mentioned we could've achieved the same and more w MongoDB. So let's use
it until I finally figure out a proper way to model data. Btw that could take
quite long given that the entire world still hasn't even approached anything
that I'd call a solution. Yeah, the world's going in the wrong direction. Look,
they call mongo non-relational database, but well they've just dropped schema in
order to make higher-order logic possible. That doesn't mean it's
non-fucking-relational. Anyways. I'll set up a mongo plus eve in a few minutes.

Oh, and on why. Eve's bad at eager loading. So it'd just yield Variable ids in
Doctypes and record ids in Doc. And flask-restless is shitcoded and expects sqla
model to have a `__tablename__`. And SQLA is culpable too --- it doesn't allow
to set tablename together with table. If tablename's set, it apparently doesn't
search for table and then finds no fields (smth like that, hadn't checked). Ugh

## Modularity w eve and mongo

The models are described as Cerberus
[Cerberus](https://github.com/pyeve/cerberus) schema (a plain data! a simple dict!)
and fed to [Eve](https://github.com/pyeve/eve).

The way we build these models is we use immutable maps from `pyrsistent` and
write model in reusable immutable pieces, which are then "added" up into a huge
model. Unfortunately I have to convert this map into a mutable python dictionary
so that Eve can use it. Perhaps I'll see later if I can eliminate the
assignments from Eve's code and push the changes upstream. That'd be great. At
the moment though it doesn't matter since it's only converted once at startup.

The actual backend resides in [`./racings_app/`](./racings_app/)
and does basically nothing. It imports a model and runs Eve. That's all.

Now I can finally move to the front side.
