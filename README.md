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
layer. E.g. we could use `eve` (see package `racings_rest`).
With REST end points we can build a frontend using some sodding js framework and
serve it as static content --- a perfect isolation between model layer and
presentation layer.
