# Copyright (C) 2014 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not
# use this file except in compliance with the License. You may obtain a copy
# of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

# An implementation of the Mafia party game state machine.

import "lib/enum" =~ [=> makeEnum]
import "unittest" =~ [=> unittest]
import "lib/entropy/entropy" =~ [=> makeEntropy :DeepFrozen]
import "lib/entropy/pcg" =~ [=> makePCG :DeepFrozen]
exports (makeMafia, DAY, NIGHT)

def [MafiaState :DeepFrozen,
     DAY :DeepFrozen,
     NIGHT :DeepFrozen] := makeEnum(["day", "night"])

    
def makeMafia(var players :Set, rng) as DeepFrozen:
    # Intial mafioso count.
    def mafiosoCount :Int := players.size() // 3

    def sample(population :List, k :(Int <= population.size())) :List:
        def n := population.size()
        def ixs := [].diverge()
        while (ixs.size() < k):
            if (!ixs.contains(def ix := rng.nextInt(n))):
                ixs.push(ix)
        return [for ix in (ixs) population[ix]]

    var mafiosos :Set := sample(players.asList(), mafiosoCount).asSet()
    var innocents :Set := players - mafiosos

    var state :MafiaState := NIGHT
    var day := 0
    var votes :Map := [].asMap()

    object mafia:
        to _printOn(out) :Void:
            def mafiaSize :Int := mafiosos.size()
            def playerSize :Int := players.size()
            out.print(`<Mafia: $playerSize players, `)
            def winner := mafia.getWinner()
            if (winner == null):
                out.print(`$state $day>`)
            else:
                out.print(`winner $winner>`)

        to getState() :MafiaState:
            return state

        to getQuorum() :Int:
            return switch (state) {
                match ==DAY { (mafiosos.size() + innocents.size() + 1) // 2}
                match ==NIGHT {mafiosos.size()}
            }

        to getMafiaCount() :Int:
            return mafiosoCount

        to getWinner():
            if (mafiosos.size() == 0):
                return "village"
            if (mafiosos.size() >= innocents.size()):
                return "mafia"
            return null

        to advance() :Str:
            if (mafia.getWinner() =~ outcome ? (outcome != null)):
                return outcome
            if ([state, day] == [NIGHT, 0]) {
                state := DAY
                day += 1
                return "It's morning on the first day."
            }
            if (mafia.lynch() =~ note ? (note != null)):
                state := switch (state) {
                    match ==DAY {NIGHT}
                    match ==NIGHT { day += 1; DAY}
                }
                votes := [].asMap()
                return note
            return `${votes.size()} votes cast.`


        to vote(player ? (players.contains(player)),
                choice ? (players.contains(choice))) :Void:
            switch (state):
                match ==DAY:
                    votes with= (player, choice)
                match ==NIGHT:
                    if (mafiosos.contains(player)):
                        votes with= (player, choice)

        to lynch() :NullOk[Str]:
            def quorum :Int := mafia.getQuorum()
            def counter := [].asMap().diverge()
            for _ => v in (votes):
                if (counter.contains(v)):
                    counter[v] += 1
                else:
                    counter[v] := 1
            traceln(`Counted votes as $counter`)

            escape ej:
                def [victim] exit ej := [for k => v in (counter) if (v >= quorum) k]
                def count := counter[victim]
                def side := mafiosos.contains(victim).pick(
                    "mafioso", "innocent")
                players without= (victim)
                mafiosos without= (victim)
                innocents without= (victim)
                return `With $count votes, $side $victim was killed.`
            catch _:
                return null

    return ["game" => mafia, "mafiosos" => mafiosos]


def sim1(assert):
    def names := ["Alice", "Bob", "Charlie",
                  "Doris", "Eileen", "Frank",
                  "Gary"]
    def rng := makeEntropy(makePCG(731, 0))
    def randName := fn { names[rng.nextInt(names.size())] }
    def [=> game, =>mafiosos] := makeMafia(names.asSet(), rng)
    assert.equal(`$game`, "<Mafia: 7 players, night 0>")
    assert.equal(mafiosos, ["Eileen", "Frank"].asSet())

    def steps := [game.advance()].diverge()
    while (game.getWinner() == null):
        # Rather than keep track of who is still in the game,
        # just catch the guard failure.
        try:
            game.vote(randName(), randName())
        catch _:
            continue
        def step := game.advance()
        if (step !~ `@n votes cast.`):
            steps.push(step)
            steps.push(`$game`)

    assert.equal(steps.snapshot(),
                 ["It's morning on the first day.",
                  "With 4 votes, innocent Alice was killed.",
                  "<Mafia: 6 players, night 1>",
                  "With 2 votes, mafioso Eileen was killed.",
                  "<Mafia: 5 players, day 2>",
                  "With 3 votes, mafioso Frank was killed.",
                  "<Mafia: 4 players, winner village>"])
unittest([sim1])
