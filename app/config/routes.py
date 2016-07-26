from system.core.router import routes


routes['default_controller'] = 'Events'
routes['POST']['/register'] = 'Events#register'
routes['POST']['/login'] = 'Events#login'
routes['GET']['/success'] = 'Events#success'
routes['GET']['/logout'] = 'Events#logout'
