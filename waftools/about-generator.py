#!/usr/bin/env python
# encoding: utf-8
# Dominik Fischer, 2014 (XZS)

"""
Automatically fills a template from an authors file.

Example::

    bld(features = 'authors',
        authors = 'AUTHORS',
        template = 'template.txt.in',
        target = 'template.txt'
    )

This will create a file "template.txt", by copying "template.txt.in", replacing
all occurrences of "${heading}" with the names found under the correspondingly
named headline in "AUTHORS".
"""

from waflib.TaskGen import feature
from waflib.Task import Task
from string import Template
from xml.sax.saxutils import escape

class split:
  """
  Dissects an iterable starting a new iterator whenever
  a separator is encountered, discarding the separator.
  """
  def __init__(self, iterable, separator):
    self.separator = separator
    self.it = iter(iterable)
  def __iter__(self):
    return self
  def _step(self):
    self.current = next(self.it)
  def __next__(self):
    self._step()
    return self._subiter()
  def _subiter(self):
    while self.current != self.separator:
      yield self.current
      self._step()

class template(Task):
  def run(self):
    groups = {group[0].replace(' ', '_'): '\n'.join(
      escape(person) for person in group[2:]
    ) for group in (
      list(category) for category in split(
        self.inputs[0].read().splitlines(),
        ''))}
    self.outputs[0].write(
      Template(self.inputs[1].read()).safe_substitute(groups))

@feature('authors')
def authors_template(gen):
  path = gen.path
  gen.create_task('template',
      [path.find_node(gen.authors), path.find_node(gen.template)],
      path.find_node(gen.authors))
