# Copyright (c) The University of Edinburgh 2014-2015
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

'''
Counts words produced by a WordProducer.
'''

from dispel4py.workflow_graph import WorkflowGraph

from dispel4py.examples.graph_testing.testing_PEs\
    import IntegerProducer, RepeatablePrimeSieve

producer = IntegerProducer(2, 1000)
sieve = RepeatablePrimeSieve()
graph = WorkflowGraph()
graph.connect(producer, 'output', sieve, RepeatablePrimeSieve.INPUT_NUMBER_LINE)

prev = sieve
for i in range(1, 168):
    sieve = RepeatablePrimeSieve()
    graph.connect(prev, RepeatablePrimeSieve.OUTPUT_NUMBER_LINE, sieve, RepeatablePrimeSieve.INPUT_NUMBER_LINE)
    prev = sieve
