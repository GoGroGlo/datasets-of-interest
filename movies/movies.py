import pandas
import xlsxwriter


# import db
movies_init = pandas.read_excel('movies.xlsx', sheet_name='movies')


# quick look at movies
# print(movies.head(10), '\n')
# print(movies.info(), '\n')

# RangeIndex: 15325 entries, 0 to 15324
# Data columns (total 8 columns):
#  #   Column        Non-Null Count  Dtype
# ---  ------        --------------  -----
#  0   id            15325 non-null  int64
#  1   metascore     15325 non-null  int64
#  2   rating        14201 non-null  object
#  3   release_date  15325 non-null  object
#  4   sort_no       15325 non-null  int64
#  5   summary       15322 non-null  object
#  6   title         15325 non-null  object
#  7   user_score    15325 non-null  object


# trim movies table by returning only relevant columns
movies = pandas.DataFrame()
movies['title'] = movies_init['title']
movies['release_date'] = movies_init['release_date']
movies['metascore'] = movies_init['metascore']
movies['rating'] = movies_init['rating']


# quick look at movies
print('---------- INITIAL MOVIES TABLE ---------')
print(movies.head(10), '\n')


# make rating_mapping table
rating_mapping = pandas.read_excel('movies.xlsx', sheet_name='mapping')
rating_mapping.set_index('rating', inplace=True)


#quick look at rating_mapping
print('---------- RATING MAPPINGS ---------')
print(rating_mapping, '\n')


# create column new_rating by translating rating into new_rating
movies['new_rating'] = movies['rating'].map(rating_mapping['new_rating'])


# sort by new_rating, then metascore
movies.sort_values(['new_rating', 'metascore'], ascending=[True, False], inplace=True)


# quick look at movies - should have new_rating
print('---------- MOVIES TABLE WITH NEW RATINGS ---------')
print(movies.head(10), '\n')


# create excel book where we'll make one sheet per new_rating
excel = pandas.ExcelWriter('top_10_movies_per_rating.xlsx', engine='xlsxwriter')


# retrieve unique new_ratings
cols = movies['new_rating'].unique().tolist()

print('---------- UNIQUE NEW_RATINGS ----------')
print(cols, '\n')

for col in cols:
	# create a DF for every top 10 movie of a given rating 
	col_df = movies[movies['new_rating']==col]
	print(f'---------- TOP 10 {col} MOVIES ----------')
	print(col_df.head(10), '\n')
	col_df = col_df.head(10)
	# then save this to a sheet within the excel book
	col_df.to_excel(excel, sheet_name=f'Top 10 {col} Movies', index=False)
	print(f'Top 10 {col} Movies has been printed in file top_10_movies_per_rating.xlsx\n')


# close excel book
excel.book.close()