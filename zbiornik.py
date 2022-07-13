import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import numpy as np

def sym(z1,z2,z3,deszcz, hm, hd, pow, Tpp, kpp, Tdd, Tii, Um, Qm):
    h0 = 0.0
    h = [h0]
    hmin = 0.0 # wielkosc minimalnla
    hust = hd
    hmax = hm
    #hust = 1.0 # wielkosc zadana
    #hmax = 5 # wielkosc maksymalna

    e = [0]
    eSum = e[0]

    uchyb = 0
    tmp_hmax = 0
    przeregulowanie = 0
    dokladnosc = eSum
    koszty = 0
    czas_regulacji = 0

    A = pow
    #A = 2

    Qdmin = 0
    Qdmax = Qm
    #Qdmax = 0.005
    Qd = [0.0]
    Qo = [0.0]
    Qo1 = [0.0]
    Qo2 = [0.0]
    Qo3 = [0.0]

    #Tp = 0.1 # okres probkowania
    Tp = Tpp
    godz = 5
    tsim = godz * 3600
    N = int(tsim / Tp)

    kp = kpp
    Ti = Tii
    Td = Tdd
    #kp = 0.015 # wzmocnienie regulatora
    #Ti = 0.25
    #Td = 0.01

    u = [0.0]
    umin = 0.0
    umax = Um
    #umax = 10.0

    q1 = z1
    q2 = z2
    q3 = z3
    #q1 = 0.002
    #q2 = 0.0007
    #q3 = 0.0003
    s = []
    s1 = []
    s2 = []
    s3 = []
    prognoza = deszcz
    #prognoza = [0.0, 0.001, 0.001, 0.0, 0.003]
    #prognoza = [0.0, 0.0, 0.0, 0.0, 0.0]


    for pogoda in range(len(prognoza)):
           s1_tmp = (q1 - prognoza[pogoda]) / math.sqrt(2 * 9.81 * hust)
           if s1_tmp < 0:
                  s1_tmp = 0
           s1.append(s1_tmp)
           s2_tmp = (q2 - prognoza[pogoda]) / math.sqrt(2 * 9.81 * hust)
           if s2_tmp < 0:
                  s2_tmp = 0
           s2.append(s2_tmp)
           s3_tmp = (q3 - prognoza[pogoda]) / math.sqrt(2 * 9.81 * hust)
           if s3_tmp < 0:
                  s3_tmp = 0
           s3.append(s3_tmp)
           s.append(s1_tmp + s2_tmp + s3_tmp)

    for i in range(godz):
           for n in range(int(N / godz)):
                  s_tmp = s[i]
                  s1_tmp = s1[i]
                  s2_tmp = s2[i]
                  s3_tmp = s3[i]

                  eLast = hust - h[-1]
                  e.append(eLast)
                  eSum += eLast

                  tmp_u = kp * (eLast + (Tp / Ti) * eSum + (Td / Tp) * (eLast - e[-2]))
                  uLast = umin if tmp_u < umin else umax if tmp_u > umax else tmp_u
                  u.append(uLast)

                  tmp_qd = ((Qdmin - Qdmax) / (umin - umax)) * uLast + (Qdmin - (((Qdmin - Qdmax) / (umin - umax)) * umin))
                  QdLast = Qdmin if tmp_qd < Qdmin else Qdmax if tmp_qd > Qdmax else tmp_qd
                  Qd.append(QdLast)

                  QoLast = s_tmp * math.sqrt(2 * 9.81 * h[-1])
                  Qo.append(QoLast)
                  tmp = s1_tmp * math.sqrt(2 * 9.81 * h[-1])
                  Qo1.append(tmp)
                  tmp = s2_tmp * math.sqrt(2 * 9.81 * h[-1])
                  Qo2.append(tmp)
                  tmp = s3_tmp * math.sqrt(2 * 9.81 * h[-1])
                  Qo3.append(tmp)

                  tmp_h = (1 / A) * (-1 * QoLast + QdLast) * Tp + h[-1]
                  h.append(hmin if tmp_h < hmin else hmax if tmp_h > hmax else tmp_h)
                  uchyb = e[-1]
                  if tmp_h > tmp_hmax:
                      tmp_hmax = tmp_h
                      przeregulowanie = ((tmp_hmax - hust)*100 / hust)
                  dokladnosc = eSum
                  koszty = koszty + uLast
                  if tmp_h <= 0.95*hust or tmp_h >= 1.05*hust:
                      czas_regulacji = n*Tp/60


    h_data = np.array(h)
    hust_data = np.full(N + 1, hust)
    qd_data = np.array(Qd)
    qo_data = np.array(Qo)
    qo1_data = np.array(Qo1)
    qo2_data = np.array(Qo2)
    qo3_data = np.array(Qo3)

    u_data = np.array(u)
    x = np.linspace(0, N, N + 1, dtype=np.int32)
    x = x / (Tp ** -1)
    x = x / 3600

    fig = make_subplots(
           rows=5, cols=1,
           subplot_titles=(
                  "Wartość natężenia dopływu i odpływu w zależności od czasu",
                  "Wartość poziomu substancji w zbiorniku w zależności od czasu",
                  "Wartość natężenia odpływu nr.1",
                  "Wartość natężenia odpływu nr.2",
                  "Wartość natężenia odpływu nr.3"
           )
    )

    fig.add_trace(
           go.Scatter(x=x, y=qd_data,
                      mode='lines',
                      name='Qd(n)'
                      ),
           row=1, col=1
    )

    fig.add_trace(
           go.Scatter(x=x, y=qo_data,
                      mode='lines',
                      name='Qo(n)'
                      ),
           row=1, col=1
    )

    fig.add_trace(
           go.Scatter(x=x, y=h_data,
                      mode='lines',
                      name='h(n)'
                      ),
           row=2, col=1
    )

    fig.add_trace(
           go.Scatter(x=x, y=hust_data,
                      mode='lines',
                      name='h ust',
                      line=dict(dash='dash')
                      ),
           row=2, col=1
    )

    fig.add_trace(
           go.Scatter(x=x, y=qo1_data,
                      mode='lines',
                      name='Qo1(n)'
                      ),
           row=3, col=1
    )

    fig.add_trace(
           go.Scatter(x=x, y=qo2_data,
                      mode='lines',
                      name='Qo2(n)'
                      ),
           row=4, col=1
    )

    fig.add_trace(
           go.Scatter(x=x, y=qo3_data,
                      mode='lines',
                      name='Qo3(n)'
                      ),
           row=5, col=1
    )

    fig.update_xaxes(title_text="t[h]", row=5, col=1)

    fig.update_yaxes(title_text="Q[m^3/s]", row=1, col=1)
    fig.update_yaxes(title_text="h[m]", row=2, col=1)
    fig.update_yaxes(title_text="Q[m^3/s]", row=3, col=1)
    fig.update_yaxes(title_text="Q[m^3/s]", row=4, col=1)
    fig.update_yaxes(title_text="Q[m^3/s]", row=5, col=1)
    fig.update_layout(template='plotly_dark')

    fig.write_html("./static/plot.html")

    return {'uchyb':round(uchyb,2), 'przeregulowanie':round(przeregulowanie,2),
            'dokladnosc':round(dokladnosc,0),'koszty':round(koszty,0),'czas_regulacji' :round(czas_regulacji,0)}
#sym(0.003,0.0005,0.0005,[0,0,0,0,0.0001])