Angles API
==========

.. py:module:: thcolor.angles

Some color representations use angles as some of their properties. The base
class for angles is the following:

.. autoclass:: Angle
	:members: asdegrees, asgradians, asradians, asturns, asprincipal, fromtext

Subclasses are the following:

.. autoclass:: DegreesAngle
	:members: degrees

.. autoclass:: GradiansAngle
	:members: gradians

.. autoclass:: RadiansAngle
	:members: radians

.. autoclass:: TurnsAngle
	:members: turns
