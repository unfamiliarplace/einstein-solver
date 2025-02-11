# einstein-solver
A solver for Einstein puzzles.

## Usage

Although the solver is fairly powerful, the "UX" is not very refined and requires some finagling.

1. Create a new game file under games. You can see some examples in the repo. A JSON game object has two keys:
   
    -  `kinds`. This is a list of kind objects. Each kind object has two keys:  
        - `name`, a string identifying the kind, e.g. `'Person'` or `'Food'`.
        - `things`, a list of strings identifying the things of that kind, e.g. `['Jason', 'Richard']`.
  
    - `clues`. This is a list of clues. Each clue is a list of rules.
    (This is for organization since the original puzzles sometimes have multiple logical rules in one clue.) 
    A rule, finally, is a list of function objects. A function has two keys:
        - `func`. The available functions are these:  
            - `link` and `-link` (not `link`): Whether a direction relationship exists between two things. For example, if we know that `Jason`'s favourite food is `Pizza`, we could mark `Jason` and `Pizza` as linked.
            - `same` and `-same` (not `same`): Whether two things are known to be the same. For example, if we know that `Jason`'s favourite food is `Pizza`, we could mark `Jason::Food` and `Pizza` as being the same.
            - `not`, `and`, `or`, `nor`, `nand`, `xor`: boolean operators whose arguments will be lists of rules instead of things. All of these can take arbitrary numbers of rules.
            - sorting functions:
              - `<` `>` `<=` `>=`: Whether two or more objects can be numerically sorted in this order. For example, if we know that `Jason`'s favourite month comes before `Richard`'s, we could mark `Jason::Month` and `Richard::Month` as being in a `<` relationship.
              - `adj`, `adj<`, `adj>` (adacent): Whether two or more objects are adjacent when ordered. For example, if a set of things is `1`, `3`, `6`, and `8`, then `adj` with arguments `3` and `6` is `True`.
              - These can all be prefixed by `-` to stipulate their negation.
              - These can all be suffixed by `A` to use alphabetic sorting instead of numerical sorting.
        - `args`. A list of symbols or, for the boolean operators, rules. A symbol can be the name of a thing, e.g. `Jason`, or it can be a relationship, e.g. `Jason::Food` (the `Food` asssociated with `Jason`). Relationships can be any depth.

2. Run `main.py` and select your game. All possible solutions will be presented one at a time.

## Example

Let's look at [`timetoquit.pdf`](src/games/sources/timetoquit.pdf). First, the kinds are as follows:

```
Person: Bianca, Charlie, Ricky, Roger, Trenton
Magazine: Fortune, Newsweek, People, Time, US Weekly
Fruit: Apples, Boysenberries, Guavas, Kiwis, Strawberries
Last Day: 01-03, 05-28, 07-08, 08-08, 09-23
```

Note that we use numbers for the dates rather than the month names, because glancing ahead, we see that some of the clues require them to be sortable.

Next, let's translate some of the rules.

1. "The 5 people were the person who grows kiwis, the employee whose last day will be July 8, the People subscriber, Trenton, and the person who grows guavas."

This means that these are five different people. Therefore, none of these things are linked with any other. When we use `link` with more than two things, *all* of them must be linked with each other. When we use `-link`, no links must exist between *any* pair of items. So that's perfect for our case.

```
"func": "-link",
"args": ["Kiwis", "07-08", "People", "Trenton", "Guavas"]
```

2. "The Time subscriber will leave before the Newsweek subscriber."

Note that this doesn't mean that `Time` is less than `Newsweek`, but that whoever reads `Time` has a `Last Day` before that of whoever reads `Newsweek`. We can use symbol resolutions to express this:

```
"func": "<",
"args": ["Time::Last Day", "Newsweek::Last Day"]
```

3. "The Time subscriber doesn't grow guavas."

This means that we know that the `Fruit` associated with `Time` is not `Guavas`; i.e., they are not the same thing.

```
"func": "-same",
"args": ["Time::Fruit", "Guavas"]
```

4. "The Time subscriber will leave before Ricky."

Easy-peasy:

```
"func": "<",
"args": ["Time::Last Day", "Ricky::Last Day"]
```

5. "Of Trenton and the person who grows apples, one is leaving the company on September 2 and the other subscribed to US Weekly."

OK, now this one is tough. It seems to mean that either Trenton is leaving on September 2 `and` the apple-grower is subscribed to US Weekly, or else (`xor`) Trenton is subscribed to US Weekly `and` the apple-grower is leaving on September 2. This leads to a triply nested structure using `link` at the bottom level:

```
"func": "xor",
"args": [
    {
        "func": "and",
        "args": [
            {
                "func": "link",
                "args": ["Trenton", "09-02"]
            },
            {
                "func": "link",
                "args": ["Apples", "US Weekly"]
            }
        ]
    },
    {
        "func": "and",
        "args": [
            {
                "func": "link",
                "args": ["Apples", "09-02"]
            },
            {
                "func": "link",
                "args": ["Trenton", "US Weekly"]
            }
        ]
    }
]
```

This is not actually quite enough, though. These rules don't yet capture one implication of the clue: that Trenton is not the apple-grower and that the person who subscribed to US Weekly did not leave on September 2. We can thus two more rules to our clue:

```
"func": "-link",
"args": ["Trenton", "Apples"]
```

and:

```
"func": "-link",
"args": ["09-23", "US Weekly"]
```

P.S. Note that having two rules is the same as having one rule that uses `and` to join two subrules. Also, if you think about it, saying `-link` with arguments `Trenton` and `Apples` is the same as saying `-same` with arguments `Trenton::Fruit` and `Apples` or with arguments `Trenton` and `Apples::Person`. There are often multiple ways to say something. You might observe that `same` is more specific (and it also runs faster), but it would be much harder to construct our first clue above without `link`, because we would have to explicitly enumerate every pair of relationships.

The rest of the clues should be comprehensible from the above start. To see a full translation (and the whole structure of the JSON file), read [`timetoquit.json`](src/games/timetoquit.json). Try it out by running `main.py` and selecting `timetoquit`.

## Dependencies

* `tabulate` for pretty-printing solutions
* `progressbar` for attractive display of solution-finding progress


## TODO

* Make an easier way to create game files, perhaps a graphic interface or a text file notation.
* Remove the `progressbar` dependency, providing a simple print progress statement if it's not present.
* Remove the `tabulate` dependency, providing a simple handmade table if it's not present.