import pandas as pd
import streamlit as st


st.set_page_config(page_title="Калькулятор особистого бюджету", page_icon="💰")

st.title("💰 Калькулятор особистого бюджету")
st.write("Введіть дохід і витрати за місяць, щоб побачити фінансовий результат.")

st.header("1. Введення даних")

income = st.number_input(
    "Місячний дохід",
    min_value=0.0,
    value=0.0,
    step=100.0,
)

st.subheader("Категорії витрат")

food = st.number_input("Їжа", min_value=0.0, value=0.0, step=50.0)
transport = st.number_input("Транспорт", min_value=0.0, value=0.0, step=50.0)
entertainment = st.number_input("Розваги", min_value=0.0, value=0.0, step=50.0)
housing = st.number_input("Житло / Комунальні", min_value=0.0, value=0.0, step=50.0)
other = st.number_input("Інше", min_value=0.0, value=0.0, step=50.0)

if st.button("Розрахувати бюджет"):
    expenses_data = {
        "Категорія": ["Їжа", "Транспорт", "Розваги", "Житло / Комунальні", "Інше"],
        "Сума": [food, transport, entertainment, housing, other],
    }

    df = pd.DataFrame(expenses_data)

    total_expenses = df["Сума"].sum()
    balance = income - total_expenses

    if balance > 0:
        status = "Профіцитний бюджет ✅"
    elif balance == 0:
        status = "Збалансований бюджет ⚖️"
    else:
        status = "Дефіцитний бюджет ⚠️"

    st.header("2. Результати")
    st.subheader("Таблиця витрат")
    st.dataframe(df, use_container_width=True)

    st.subheader("Підсумки")
    st.write(f"**Загальні витрати:** {total_expenses:.2f} грн")
    st.write(f"**Залишок коштів:** {balance:.2f} грн")
    st.write(f"**Статус бюджету:** {status}")

    st.subheader("Графік витрат")
    chart_data = df.set_index("Категорія")
    st.bar_chart(chart_data)

    save_csv = st.checkbox("Зберегти результати у CSV")

    if save_csv:
        result_df = df.copy()
        result_df.loc[len(result_df)] = ["ДОХІД", income]
        result_df.loc[len(result_df)] = ["ЗАГАЛЬНІ ВИТРАТИ", total_expenses]
        result_df.loc[len(result_df)] = ["ЗАЛИШОК", balance]

        result_df.to_csv("monthly_budget_results.csv", index=False, encoding="utf-8-sig")
        st.success("Результати збережено у файл monthly_budget_results.csv")
