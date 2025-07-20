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
    
    # Створюємо заголовок з посиланням на рік, якщо він вказаний
    title = 'Кількість прочитаних книг за місяцями'
    if start_year is not None:
        current_year = pd.Timestamp.now().year
        if start_year == current_year:
            title += f' у {start_year} році'
        else:
            title += f' починаючи з {start_year} року'
    
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
    
    # Створюємо заголовок з посиланням на рік, якщо він вказаний
    title = 'Кількість прочитаних книг за днями тижня'
    if start_year is not None:
        current_year = pd.Timestamp.now().year
        if start_year == current_year:
            title += f' у {start_year} році'
        else:
            title += f' починаючи з {start_year} року'
    
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
    
    # Створюємо заголовок з посиланням на рік, якщо він вказаний
    title = 'Середні оцінки та кількість сторінок книг'
    if start_year is not None:
        current_year = pd.Timestamp.now().year
        if start_year == current_year:
            title += f' у {start_year} році'
        else:
            title += f' починаючи з {start_year} року'
    
    graph_data = {
        'data': [
            {
                'x': years,
                'y': ratings,
                'name': 'Середня оцінка',
                'type': 'scatter',
                'mode': 'lines+markers',
                'line': {'color': 'rgb(55, 83, 109)'}
            },
            {
                'x': years,
                'y': pages,
                'name': 'Середня кількість сторінок',
                'type': 'scatter',
                'mode': 'lines+markers',
                'yaxis': 'y2',
                'line': {'color': 'rgb(255, 133, 27)'}
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
                'range': [max(0, min(ratings) * 0.8) if ratings else 0, max(ratings) * 1.2]  # Починаємо з 80% від мінімального значення
            },
            'yaxis2': {
                'title': 'Середня кількість сторінок',
                'rangemode': 'tozero',
                'side': 'right',
                'overlaying': 'y',
                'showgrid': False,
                'tickfont': {'color': 'rgb(255, 133, 27)'},
                'range': [max(0, min(pages) * 0.8) if pages else 0, int(max(pages) * 1.2)]  # Починаємо з 80% від мінімального значення
            },
            'plot_bgcolor': 'rgba(0,0,0,0)',
            'paper_bgcolor': 'rgba(0,0,0,0)',
            'legend': {
                'orientation': 'h',
                'y': 1.1,
                'x': 0.5,
                'xanchor': 'center'
            }
        }
    }
    
    return graph_data
