import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

def calcular_parcelas_numero(valor_total, numero_parcelas, taxa_juros_mensal, data_inicio, periodicidade):
    valor_parcela = valor_total * (taxa_juros_mensal / (1 - (1 + taxa_juros_mensal)**(-numero_parcelas)))
    juros_total = valor_parcela * numero_parcelas - valor_total

    datas_vencimento = [data_inicio]
    if periodicidade == 'Mensal':
        for i in range(1, numero_parcelas):
            datas_vencimento.append(datas_vencimento[i-1] + timedelta(days=30))
    elif periodicidade == 'Quinzenal':
        for i in range(1, numero_parcelas):
            datas_vencimento.append(datas_vencimento[i-1] + timedelta(days=15))
    elif periodicidade == 'Semanal':
        for i in range(1, numero_parcelas):
            datas_vencimento.append(datas_vencimento[i-1] + timedelta(days=7))

    parcelas = []
    saldo_devedor = valor_total
    for i in range(numero_parcelas):
        amortizacao = valor_parcela - saldo_devedor * taxa_juros_mensal
        parcelas.append({'Parcela': i+1, 'Data Vencimento': datas_vencimento[i], 'Valor Parcela': valor_parcela, 
                         'Juros': saldo_devedor * taxa_juros_mensal, 'Amortização': amortizacao, 'Saldo Devedor': saldo_devedor})
        saldo_devedor -= amortizacao

    return valor_parcela, juros_total, pd.DataFrame(parcelas)

def calcular_parcelas_valor(valor_total, valor_parcela, taxa_juros_mensal, data_inicio, periodicidade):
    parcelas = []
    saldo_devedor = valor_total
    data_vencimento = data_inicio
    while saldo_devedor > 0:
        amortizacao = valor_parcela - saldo_devedor * taxa_juros_mensal
        parcelas.append({'Data Vencimento': data_vencimento, 'Valor Parcela': valor_parcela, 
                         'Juros': saldo_devedor * taxa_juros_mensal, 'Amortização': amortizacao, 'Saldo Devedor': saldo_devedor})
        saldo_devedor -= amortizacao
        if periodicidade == 'Mensal':
            data_vencimento += timedelta(days=30)
        elif periodicidade == 'Quinzenal':
            data_vencimento += timedelta(days=15)
        elif periodicidade == 'Semanal':
            data_vencimento += timedelta(days=7)

    return pd.DataFrame(parcelas)

st.title('Calculadora Financeira da Confiança')

modo_calculo = st.radio("Modo de cálculo:", options=['Número de parcelas', 'Valor mínimo da parcela'])

if modo_calculo == 'Número de parcelas':
    valor_total = st.number_input('Valor total:', min_value=0.01, step=0.01)
    numero_parcelas = st.number_input('Número de parcelas:', min_value=1, step=1, format='%d')
    taxa_juros_mensal = st.number_input('Taxa de juros mensal (%):', min_value=0.01, step=0.01)
    periodicidade = st.radio("Periodicidade dos pagamentos:", options=['Mensal', 'Quinzenal', 'Semanal'])

    data_inicio = st.date_input('Data de início do financiamento:', min_value=datetime.now())

    if st.button('Calcular'):
        valor_parcela, juros_total, df = calcular_parcelas_numero(valor_total, numero_parcelas, taxa_juros_mensal / 100, data_inicio, periodicidade)
        st.write(f'Valor de cada parcela: R$ {valor_parcela:.2f}')
        st.write(f'Total de juros pagos: R$ {juros_total:.2f}')
        st.write(df)

        # total_parcela = df['Valor Parcela'].sum()
        # total_juros = df['Juros'].sum()
        # st.write(f'Soma total das parcelas: R$ {total_parcela:.2f}')
        # st.write(f'Soma total dos juros: R$ {total_juros:.2f}')

        if st.button('Nova simulação'):
            df.to_excel('resultados_financiamento.xlsx', index=False)
            st.success('Arquivo Excel gerado com sucesso!')

elif modo_calculo == 'Valor mínimo da parcela':
    valor_total = st.number_input('Valor total:', min_value=0.01, step=0.01)
    valor_minimo_parcela = st.number_input('Valor mínimo da parcela:', min_value=0.01, step=0.01)
    taxa_juros_mensal = st.number_input('Taxa de juros mensal (%):', min_value=0.01, step=0.01)
    periodicidade = st.radio("Periodicidade dos pagamentos:", options=['Mensal', 'Quinzenal', 'Semanal'])

    data_inicio = st.date_input('Data de início do financiamento:', min_value=datetime.now())

    if st.button('Calcular'):
        df = calcular_parcelas_valor(valor_total, valor_minimo_parcela, taxa_juros_mensal / 100, data_inicio, periodicidade)
        st.write(df)

        total_parcela = df['Valor Parcela'].sum()
        total_juros = df['Juros'].sum()
        # st.write(f'Soma total das parcelas: R$ {total_parcela:.2f}')
        # st.write(f'Soma total dos juros: R$ {total_juros:.2f}')

        if st.button('Nova simulação'):
            df.to_excel('resultados_financiamento.xlsx', index=False)
            st.success('Arquivo Excel gerado com sucesso!')