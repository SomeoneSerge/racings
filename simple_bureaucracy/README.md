# simple_bureaucracy

An attempt to model the document management.
That includes managing data, IO and UI generation.

There are several points for this effort:
1.  The problems arising in the `racings` app are common and trivial so the
    solution ought to be reusable.
2.  The UI should be automatically generated. The reason any LaTeX document
    looks by-default so much better than any piece of crap produced by this
    silly microsoft word bullshit is that LaTeX strives to optimize the
    entire document's layout so as to achieve the maximal "beauty" whereas in
    word you take care of each single character yourself. This leads to
    iconsistency of an overall picture.

## Racings app example

We'd like to specify the app using plain datastructures and then produce the details
from the specification.
