from wtforms import Form, BooleanField, StringField, validators, SelectField

levels = ['None',
          'A1 - Beginner',
          'A2.1 - Low Intermediate',
          'A2.2 - Mid Intermediate',

          'B1 - Intermediate High',
          'B2.1 - Advanced Low',
          'B2.2 - Advanced Mid',
          'B2.3 - Advanced High',

          'C1 - Superior',
          'C2 - Distinguished']

levels_no_letters = ['None',
                     'Beginner',
                     'Low Intermediate',
                     'Mid Intermediate',

                     'Intermediate High',
                     'Advanced Low',
                     'Advanced Mid',
                     'Advanced High',

                     'Superior',
                     'Distinguished']

cefr_levels = ['None',
               'A1 - Beginner',
               'A2 - Elementary',
               'B1 - Intermediate',
               'B2 - Upper Intermediate',
               'C1 - Advanced ',
               'C2 - Proficient']

cefr_levels_no_letters = ['None',
                          'Beginner',
                          'Elementary',
                          'Intermediate',
                          'Upper Intermediate',
                          'Advanced ',
                          'Proficient']

one_to_ten = [(each, each) for each in cefr_levels_no_letters]


class AccountSettingsForm(Form):
    name = StringField('Name ', [validators.Length(min=2, max=25)])
    email = StringField('Email ', [validators.Length(min=6, max=35)])

    native_language = SelectField('Native Language', choices=[
        ('zh-CN', 'Chinese'),
        ('da', 'Danish'),
        ('nl', 'Dutch'),
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('ro', 'Romanian')
    ])

    learned_language = SelectField('Learned Language', choices=[
        ('zh-CN', 'Chinese'),
        ('da', 'Danish'),
        ('nl', 'Dutch'),
        ('en', 'English'),
        ('fr', 'French'),
        ('de', 'German'),
        ('es', 'Spanish'),
        ('ro', 'Romanian')
    ])


    french = SelectField('French: ', choices=one_to_ten)
    english = SelectField('English: ', choices=one_to_ten)
    dutch = SelectField('Dutch: ', choices=one_to_ten)
    italian = SelectField('Italian: ', choices=one_to_ten)
    german = SelectField('German: ', choices=one_to_ten)
    spanish = SelectField('Spanish: ', choices=one_to_ten)
