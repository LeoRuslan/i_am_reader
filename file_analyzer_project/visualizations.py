import pandas as pd


def plot_books_per_year(df_read, **kwargs):
    """
    Створює дані для графіка кількості прочитаних книг за роками.

    Parameters:
        df_read (pd.DataFrame): DataFrame з даними про прочитані книги.
        **kwargs: Додаткові параметри для налаштування графіка.
            start_year (int, optional): Рік, з якого починати аналіз. 
                                     За замовчуванням 2018. Якщо None, аналізує всі доступні роки.

    Returns:
        dict: Словник з даними для графіка Plotly.
    """
    # Отримуємо start_year з kwargs або використовуємо значення за замовчуванням 2018
    start_year = kwargs.get('start_year', 2018)
    
    # Фільтруємо дані за роком, якщо вказано start_year
    if start_year is not None:
        df_filtered = df_read[df_read['year_read'] >= start_year]
    else:
        df_filtered = df_read
    
    # Рахуємо кількість книг за роками
    books_per_year = df_filtered['year_read'].value_counts().sort_index()
    
    years = books_per_year.index.astype(int).astype(str).tolist()
    # Конвертуємо значення у Python int
    values = [int(v) for v in books_per_year.values.tolist()]

    graph_data = {
        'data': [{
            'x': years,
            'y': values,
            'type': 'bar',
            'text': values,
            'textposition': 'auto',
            'texttemplate': '%{y}',
            'hoverinfo': 'x+text',
            'marker': {'color': 'rgb(59, 117, 175)'}
        }],
        'layout': {
            'title': 'Кількість прочитаних книг за роками',
            'xaxis': {
                'title': 'Рік',
                'type': 'category',
                'tickmode': 'array',
                'tickvals': years,
                'ticktext': years
            },
            'yaxis': {
                'title': 'Кількість книг',
                'rangemode': 'tozero'
            },
            'showlegend': False
        }
    }
    return graph_data


def plot_books_per_month(df_read, **kwargs):
    """
    Створює дані для графіка кількості прочитаних книг за місяцями.

    Parameters:
        df_read (pd.DataFrame): DataFrame з даними про прочитані книги.
        **kwargs: Додаткові параметри для налаштування графіка.
            start_year (int, optional): Рік, з якого починати аналіз. 
                                     За замовчуванням 2018. Якщо None, аналізує всі доступні роки.

    Returns:
        dict: Словник з даними для графіка Plotly.
    """
    # Отримуємо start_year з kwargs або використовуємо значення за замовчуванням 2018
    start_year = kwargs.get('start_year', 2018)
    
    # Фільтруємо дані за роком, якщо вказано start_year
    if start_year is not None:
        df_filtered = df_read[df_read['year_read'] >= start_year].copy()
    else:
        df_filtered = df_read.copy()
    
    # Створюємо словник для перекладу номерів місяців у назви
    month_names = {
        1: 'Січень', 2: 'Лютий', 3: 'Березень', 4: 'Квітень',
        5: 'Травень', 6: 'Червень', 7: 'Липень', 8: 'Серпень',
        9: 'Вересень', 10: 'Жовтень', 11: 'Листопад', 12: 'Грудень'
    }
    
    # Рахуємо кількість книг за місяцями
    books_per_month = df_filtered['month_read'].value_counts().sort_index()
    
    # Перетворюємо індекси (номери місяців) у назви
    months = [month_names[i] for i in books_per_month.index]
    # Конвертуємо значення у Python int
    values = [int(v) for v in books_per_month.values.tolist()]
    
    # Заголовок графіка
    title = 'Кількість прочитаних книг за місяцями'
    if start_year is not None and start_year == pd.Timestamp.now().year:
        title += f' у {start_year} році'
    
    graph_data = {
        'data': [{
            'x': months,
            'y': values,
            'type': 'bar',
            'text': values,
            'textposition': 'auto',
            'texttemplate': '%{y}',
            'hoverinfo': 'x+text',
            'marker': {'color': 'rgb(55, 83, 109)'}
        }],
        'layout': {
            'title': title,
            'xaxis': {
                'title': 'Місяць',
                'type': 'category',
                'tickmode': 'array',
                'tickvals': months,
                'ticktext': months,
                'tickangle': -45
            },
            'yaxis': {
                'title': 'Кількість книг',
                'rangemode': 'tozero'
            },
            'showlegend': False,
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
        }
    }
    
    return graph_data

def plot_books_by_weekday(df_read, **kwargs):
    """
    Створює дані для графіка кількості прочитаних книг за днями тижня.

    Parameters:
        df_read (pd.DataFrame): DataFrame з даними про прочитані книги.
        **kwargs: Додаткові параметри для налаштування графіка.
            start_year (int, optional): Рік, з якого починати аналіз. 
                                     За замовчуванням 2018. Якщо None, аналізує всі доступні роки.

    Returns:
        dict: Словник з даними для графіка Plotly.
    """
    # Отримуємо start_year з kwargs або використовуємо значення за замовчуванням 2018
    start_year = kwargs.get('start_year', 2018)
    
    # Фільтруємо дані за роком, якщо вказано start_year
    if start_year is not None:
        df_filtered = df_read[df_read['year_read'] >= start_year].copy()
    else:
        df_filtered = df_read.copy()
    
    # Створюємо словник для перекладу номерів днів тижня у назви
    day_names = {
        0: 'Понеділок', 1: 'Вівторок', 2: 'Середа', 3: 'Четвер',
        4: 'П`ятниця', 5: 'Субота', 6: 'Неділя'
    }
    
    # Рахуємо кількість книг за днями тижня
    books_per_day = df_filtered['finished_week_day'].value_counts().sort_index()
    
    # Перетворюємо індекси (номери днів) у назви
    days = [day_names[i] for i in books_per_day.index]
    values = [int(v) for v in books_per_day.values.tolist()]
    
    # Заголовок графіка
    title = 'Кількість прочитаних книг за днями тижня'
    if start_year is not None and start_year == pd.Timestamp.now().year:
        title += f' у {start_year} році'
    
    graph_data = {
        'data': [{
            'x': days,
            'y': values,
            'text': values,
            'type': 'bar',
            'textposition': 'auto',
            'hoverinfo': 'x+text',
            'marker': {'color': 'rgb(55, 83, 109)'}
        }],
        'layout': {
            'title': title,
            'xaxis': {
                'title': 'День тижня',
                'type': 'category',
                'tickmode': 'array',
                'tickvals': days,
                'ticktext': days
            },
            'yaxis': {
                'title': 'Кількість книг',
                'rangemode': 'tozero'
            },
            'showlegend': False,
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'grid': True
        }
    }
    
    return graph_data

def plot_ratings_and_pages(df_read, **kwargs):
    """
    Створює дані для двоосьового графіка зі середніми оцінками та кількістю сторінок за роками.

    Parameters:
        df_read (pd.DataFrame): DataFrame з даними про прочитані книги.
        **kwargs: Додаткові параметри для налаштування графіка.
            start_year (int, optional): Рік, з якого починати аналіз. 
                                     За замовчуванням 2018. Якщо None, аналізує всі доступні роки.

    Returns:
        dict: Словник з даними для графіка Plotly.
    """
    # Отримуємо start_year з kwargs або використовуємо значення за замовчуванням 2018
    start_year = kwargs.get('start_year', 2018)
    
    # Фільтруємо дані за роком, якщо вказано start_year
    if start_year is not None:
        df_filtered = df_read[df_read['year_read'] >= start_year].copy()
    else:
        df_filtered = df_read.copy()
    
    # Рахуємо середні оцінки та кількість сторінок за роками
    ratings_by_year = df_filtered.groupby('year_read')['My Rating'].mean()
    pages_by_year = df_filtered.groupby('year_read')['Number of Pages'].mean()
    
    # Конвертуємо значення у Python int
    years = ratings_by_year.index.astype(int).astype(str).tolist()
    ratings = [float(v) for v in ratings_by_year.values.tolist()]
    pages = [int(v) for v in pages_by_year.values.tolist()]
    
    # Заголовок графіка
    title = 'Середні оцінки та кількість сторінок за роками'
    if start_year is not None and start_year == pd.Timestamp.now().year:
        title += f' у {start_year} році'
    
    graph_data = {
        'data': [
            {
                'x': years,
                'y': pages,
                'name': '',
                'type': 'bar',
                'yaxis': 'y2',
                'marker': {
                    'color': 'rgb(55, 83, 109)',
                    'opacity': 0.7
                },
                'text': pages,
                'textposition': 'auto',
                'hovertemplate': '<b>Середня к-сть сторінок:</b> %{y}<extra></extra>'
            },
            {
                'x': years,
                'y': ratings,
                'name': '',
                'type': 'scatter',
                'mode': 'lines+markers+text',
                'line': {'color': 'rgb(59, 117, 175)'},
                'text': [f'{r:.2f}' for r in ratings],
                'textposition': 'top center',
                'hovertemplate': '<b>Середня оцінка:</b> %{y:.2f}<extra></extra>'
            }
        ],
        'layout': {
            'title': title,
            'xaxis': {
                'title': 'Рік',
                'type': 'category',
                'tickmode': 'array',
                'tickvals': years,
                'ticktext': years
            },
            'yaxis': {
                'title': 'Середня оцінка',
                'rangemode': 'tozero',
                'side': 'left',
                'showgrid': True,
                # 'range': [max(0, min(ratings) * 0.8) if ratings else 0, max(ratings) * 1.2],  # Починаємо з 80% від мінімального значення
                'range': [0, max(ratings) * 1.2],  # Починаємо з 80% від мінімального значення
            },
            'yaxis2': {
                'title': 'Середня кількість сторінок',
                'rangemode': 'tozero',
                'side': 'right',
                'overlaying': 'y',
                'showgrid': False,
                'tickfont': {'color': 'rgb(255, 133, 27)'},
                'range': [0, int(max(pages) * 1.2)]  # Починаємо з 80% від мінімального значення
            },
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'showlegend': False,
            'hovermode': 'x unified'
        }
    }
    
    return graph_data


def plot_min_max_pages_per_year(df_read, **kwargs):
    """
    Створює дані для графіка з мінімальною та максимальною кількістю сторінок за роками.

    Parameters:
        df_read (pd.DataFrame): DataFrame з даними про прочитані книги.
        **kwargs: Додаткові параметри для налаштування графіка.
            start_year (int, optional): Рік, з якого починати аналіз. 
                                     За замовчуванням 2018. Якщо None, аналізує всі доступні роки.

    Returns:
        dict: Словник з даними для графіка Plotly.
    """
    start_year = kwargs.get('start_year', 2018)

    if start_year is not None:
        df_filtered = df_read[df_read['year_read'] >= start_year].copy()
    else:
        df_filtered = df_read.copy()

    # Перевіряємо, яка з колонок містить кількість сторінок
    page_columns = ['Number of Pages', 'num_pages', 'Pages']
    page_column = next((col for col in page_columns if col in df_filtered.columns), None)
    
    if page_column is None:
        # Якщо жодна з колонок не знайдена, повертаємо пустий графік
        return {
            'data': [],
            'layout': {
                'title': 'Дані про кількість сторінок відсутні',
                'plot_bgcolor': 'rgba(0,0,0,0)',
                'paper_bgcolor': 'rgba(0,0,0,0)'
            }
        }
    
    df_filtered['num_pages'] = pd.to_numeric(df_filtered[page_column], errors='coerce')
    df_filtered.dropna(subset=['num_pages'], inplace=True)
    df_filtered['num_pages'] = df_filtered['num_pages'].astype(int)
    df_filtered['year_read'] = df_filtered['year_read'].astype(int)  # Ensure years are integers

    pages_stats = df_filtered.groupby('year_read')['num_pages'].agg(['min', 'max']).sort_index()

    years = pages_stats.index.tolist()  # Already integers
    min_pages = pages_stats['min'].tolist()
    max_pages = pages_stats['max'].tolist()

    title = 'Мін. та макс. кількість сторінок за роками'
    if start_year is not None and start_year == pd.Timestamp.now().year:
        title += f' у {start_year} році'

    graph_data = {
        'data': [
            {
                'x': years,
                'y': min_pages,
                'name': 'Мін. к-сть сторінок',
                'type': 'bar',
                'marker': {'color': 'rgb(255, 133, 27)'},
                'text': [f'{p}' for p in min_pages],
                'textposition': 'outside',
                'textfont': {'size': 10},
                'hovertemplate': 'Мін. к-сть сторінок: %{y}<extra></extra>',
            },
            {
                'x': years,
                'y': max_pages,
                'name': 'Макс. к-сть сторінок',
                'type': 'bar',
                'marker': {'color': 'rgb(59, 117, 175)'},
                'text': [f'{p}' for p in max_pages],
                'textposition': 'outside',
                'textfont': {'size': 10},
                'hovertemplate': 'Макс. к-сть сторінок: %{y}<extra></extra>',
            }
        ],
        'layout': {
            'title': title,
            'xaxis': {
                'title': 'Рік',
                'tickmode': 'array',
                'tickvals': years,
                'ticktext': [str(int(year)) for year in years],  # Ensure years are displayed as integers
                'type': 'category',
            },
            'yaxis': {
                'title': 'Кількість сторінок',
                'rangemode': 'tozero',
                'title_standoff': 20
            },
            'barmode': 'group',
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'showlegend': False,
            'hovermode': 'x unified',
            'hoverlabel': {
                'align': 'left',
                'bgcolor': 'white',
                'bordercolor': 'lightgray',
                'font_size': 12,
                'namelength': -1  # Show full hover label text
            }
        }
    }
    return graph_data
