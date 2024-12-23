import discord
import yaml

with open('settings.yaml', 'r') as yamlfile:
    settings = yaml.safe_load(yamlfile)
    role_levels = settings.get('role_levels', {})
    staff_role_ids = list(role_levels.keys())
    developer = settings['developer']

def is_dev(ctx):
    return ctx.author.id in developer
    
def is_staff(ctx):
    user_role_ids = [role.id for role in ctx.author.roles]
    return any(role_id in staff_role_ids for role_id in user_role_ids)
