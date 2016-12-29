"""
List of constants to help selenium tests
========================================
"""
titles_suffix = 'CG Studio Map | {}'
titles = {
    '/': titles_suffix.format('Home'),
    '/aboutus': titles_suffix.format('About'),
    '/directory': titles_suffix.format('Directory'),
    '/directory/company/cg-studio-map-1': titles_suffix.format('CG Studio Map'),
    'github': 'GitHub - cgstudiomap/cgstudiomap',
}