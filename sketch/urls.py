from sketch import views as sketch_views

def apply_urls(app):
    app.add_url_rule('/sketch/create/', view_func=sketch_views.CreationWizard.as_view('wizard'))
    app.add_url_rule('/sketch/search/', view_func=sketch_views.SearchGamesView.as_view('search'))
    app.add_url_rule('/game/<game_key>', view_func=sketch_views.Game.as_view('game'))
    app.add_url_rule('/game/random', view_func=sketch_views.Game.as_view('random_game'), defaults={'game_key': None})
