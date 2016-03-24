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
exports (makeMafia)
def [MafiaState :DeepFrozen,
     DAY :DeepFrozen,
     NIGHT :DeepFrozen] := makeEnum(["day", "night"])

def makeMafia(var players :Set) as DeepFrozen:
    # We don't keep this value updated during play; it's just to make it
    # easier to tune/tweak the mafia/village slice.
    def mafiosoCount :Int := players.size() // 3
    var mafiosos :Set := players.slice(0, mafiosoCount)
    var innocents :Set := players.slice(mafiosoCount)

    var state :MafiaState := DAY
    var votes :Map := [].asMap()
    var lynched :Bool := false

    return object mafia:
        to _printOn(out) :Void:
            def mafiaSize :Int := mafiosos.size()
            def playerSize :Int := players.size()
            out.print(`<Mafia: $playerSize players ($mafiaSize mafiosos), `)
            def winner := mafia.getWinner()
            if (winner == null):
                out.print(`currently $state>`)
            else:
                out.print(`winner $winner>`)

        to getState() :MafiaState:
            return state

        to getQuorum() :Int:
            def voters :Int := switch (state) {
                match ==DAY {mafiosos.size() + innocents.size()}
                match ==NIGHT {mafiosos.size()}
            }
            return voters // 2

        to getMafiaCount() :Int:
            return mafiosos.size()

        to getWinner():
            if (mafiosos.size() == 0):
                return "village"
            if (mafiosos.size() >= innocents.size()):
                return "mafia"
            return null

        to advance() :Void:
            state := switch (state) {
                match ==DAY {NIGHT}
                match ==NIGHT {DAY}
            }
            lynched := false

        to vote(player ? (players.contains(player)),
                choice ? (players.contains(choice))) :Void:
            switch (state):
                match ==DAY:
                    votes with= (player, choice)
                match ==NIGHT:
                    if (mafiosos.contains(player)):
                        votes with= (player, choice)

        to lynch(quorum :Int) :Str:
            if (lynched):
                return "Lynching already happened during this round."
            lynched := true

            def counter := [].asMap().diverge()
            for _ => v in votes:
                if (counter.contains(v)):
                    counter[v] += 1
                else:
                    counter[v] := 1
            traceln(`Counted votes as $counter`)

            escape ej:
                def [victim] exit ej := [for k => v in (counter) if (v >= quorum) k]
                def count := counter[victim]
                players without= (victim)
                mafiosos without= (victim)
                innocents without= (victim)
                return `With $count votes ($quorum needed), $victim was killed.`
            catch _:
                return "Nobody was lynched."
