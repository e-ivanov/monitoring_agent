#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired

class ParamsForm(Form):
    collectionInterval = StringField('collectionInterval', validators=[DataRequired()])
    serverId = StringField('serverId', validators=[DataRequired()])
