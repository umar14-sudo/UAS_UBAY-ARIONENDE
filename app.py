import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for seaborn
sns.set(style="whitegrid")

# Judul aplikasi
st.title("Advanced Big Data Analysis App")

# Unggah file CSV
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    # Membaca dataset
    try:
        df = pd.read_csv(uploaded_file)

        # Menampilkan data
        st.subheader("Dataset")
        st.write(df)

        # Menampilkan nama kolom
        st.subheader("Column Names")
        st.write(df.columns.tolist())

        # Menampilkan beberapa baris pertama dari DataFrame
        st.subheader("Preview of the Data")
        st.write(df.head())

        # Memeriksa apakah kolom yang diperlukan ada
        required_columns = ['Job Title', 'Salary', 'Employee Residence', 'Experience Level', 'Company Size']
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            st.error(f"Missing columns in the dataset: {', '.join(missing_columns)}")
        else:
            # Menampilkan ringkasan data
            st.subheader("Data Summary")
            st.write(df.describe())

            # Analisis Gaji Rata-rata berdasarkan Judul Pekerjaan
            st.subheader("Average Salary by Job Title")
            job_title = st.selectbox("Select Job Title", df['Job Title'].unique())
            
            avg_salary = df[df['Job Title'] == job_title]['Salary'].mean()
            st.write(f"The average salary for {job_title} is: ${avg_salary:.2f}")

            # Visualisasi Gaji berdasarkan Judul Pekerjaan
            st.subheader("Salary Distribution by Job Title")
            salary_data = df.groupby('Job Title')['Salary'].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Salary', y='Job Title', data=salary_data, ax=ax)
            ax.set_title('Average Salary by Job Title')
            st.pyplot(fig)

            # Visualisasi Gaji berdasarkan Lokasi
            st.subheader("Salary Distribution by Location")
            location_data = df.groupby('Employee Residence')['Salary'].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Salary', y='Employee Residence', data=location_data, ax=ax)
            ax.set_title('Average Salary by Location')
            st.pyplot(fig)

            # Visualisasi Gaji berdasarkan Pengalaman
            st.subheader("Salary Distribution by Experience Level")
            experience_data = df.groupby('Experience Level')['Salary'].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Salary', y='Experience Level', data=experience_data, ax=ax)
            ax.set_title('Average Salary by Experience Level')
            st.pyplot(fig)

            # Visualisasi Gaji berdasarkan Ukuran Perusahaan
            st.subheader("Salary Distribution by Company Size")
            company_size_data = df.groupby('Company Size')['Salary'].mean().reset_index()
            fig, ax = plt.subplots()
            sns.barplot(x='Salary', y='Company Size', data=company_size_data, ax=ax)
            ax.set_title('Average Salary by Company Size')
            st.pyplot(fig)

            # Pilihan untuk analisis lebih lanjut
            st.subheader("Filter Data for Further Analysis")
            min_salary = st.number_input("Minimum Salary", min_value=0, value=0)
            max_salary = st.number_input("Maximum Salary", min_value=0, value=int(df['Salary'].max()))

            filtered_data = df[(df['Salary'] >= min_salary) & (df['Salary'] <= max_salary)]
            st.write("Filtered Data:")
            st.write(filtered_data)

            # Menampilkan ringkasan dari data yang difilter
            st.subheader("Filtered Data Summary")
            st.write(filtered_data.describe())

            # Fitur Rekomendasi
            st.subheader("Job Recommendations")
            user_experience = st.selectbox("Select Your Experience Level", df['Experience Level'].unique())
            user_location = st.selectbox("Select Your Location", df['Employee Residence'].unique())

            # Rekomendasi pekerjaan berdasarkan pengalaman dan lokasi
            recommendations = df[(df['Experience Level'] == user_experience) & 
                                 (df['Employee Residence'] == user_location)]

            if not recommendations.empty:
                st.write("Recommended Jobs for You:")
                st.write(recommendations[['Job Title', 'Salary', 'Company Size']])
            else:
                st.write("No job recommendations found for your selected criteria.")

    except Exception as e:
        st.error(f"Error reading the file: {e}")

else:
    st.warning("Please upload a CSV file to get started.")