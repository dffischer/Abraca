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

"authors" defaults to "AUTHORS", "template" is mandatory, and "target" can be
left out to be the same as "template" stripped from its ".in" prefix.
"""

from waflib.TaskGen import feature
from waflib.Task import Task
from string import Template
from re import compile, escape

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

REPLACEMENTS = {
    '<': '&lt;',
    '>': '&gt;',
    ' at ': '@',
    ' dot ': '.'
}

def replace(dict, text):
  """Replaces every dict key with its value."""
  regex = compile("|".join(map(escape, dict.keys())))
  return regex.sub(lambda x: dict[x.group(0)], text)

class template(Task):
  def run(self):
    groups = {group[0].replace(' ', '_'): '\n'.join(
      replace(REPLACEMENTS, person) for person in group[2:]
    ) for group in (
      list(category) for category in split(
        self.inputs[0].read().splitlines(),
        ''))}
    self.outputs[0].write(
      Template(self.inputs[1].read()).safe_substitute(groups))

@feature('authors')
def authors_template(gen):
  path = gen.path
  template = path.find_node(gen.template)
  authors = path.find_node(getattr(gen, 'authors', 'AUTHORS'))
  if gen.target == '':
    target = template.change_ext('', ext_in='.in')
  else:
    target = path.find_or_declare(gen.target)
  gen.create_task('template', [authors, template], target)
