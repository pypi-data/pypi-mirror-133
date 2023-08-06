#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pop.hub


def start():
    hub = pop.hub.Hub()
    hub.pop.sub.add(dyne_name="tree", omit_class=False)
    hub.tree.init.cli()
