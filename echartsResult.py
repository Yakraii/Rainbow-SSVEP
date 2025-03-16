# 仪表盘放结果
option = {
  series: [
    {
      type: 'gauge',
      startAngle: 180,
      endAngle: 0,
      center: ['50%', '75%'],
      radius: '90%',
      min: 0,
      max: 1,
      splitNumber: 10,
      axisLine: {
        lineStyle: {
          width: 6,
          color: [
            [0.33, '#FF6E76'],
            [0.5, '#FDDD60'],
            [1, '#7CFFB2']
          ]
        }
      },
      pointer: {
        icon: 'path://M12.8,0.7l12,40.1H0.7L12.8,0.7z',
        length: '12%',
        width: 20,
        offsetCenter: [0, '-60%'],
        itemStyle: {
          color: 'auto'
        }
      },
      axisTick: {
        length: 12,
        lineStyle: {
          color: 'auto',
          width: 2
        }
      },
      splitLine: {
        length: 20,
        lineStyle: {
          color: 'auto',
          width: 5
        }
      },
      axisLabel: {
        color: '#464646',
        fontSize: 20,
        distance: -60,
        rotate: 'tangential',
        fontFamily: '新宋体',
        fontWeight: 'bold',
        formatter: function (value) {
          if (value === 0.7) {
            return '无风险';
          } else if (value === 0.4) {
            return '中等风险';
          } else if (value === 0.2) {
            return '有风险';
          }
          return '';
        }
      },
      title: {
        offsetCenter: [0, '-10%'],
        fontSize: 20,
        fontFamily: ''
      },
      detail: {
        fontSize: 90,
        offsetCenter: [0, '-35%'],
        valueAnimation: true,
        formatter: function (value) {
          return Math.round(value * 100) + '';
        },
        color: 'inherit'
      },
      data: [
        {
          value: 0.72, # 这里要用后端的评估结果
          name: 'Grade Rating'
        }
      ]
    }
  ]
};


#横坐标=频率，纵坐标=每个频率分数*100，最后一个红色的是平均分数，加权求得，分别占比是30+30+15+15+10
option = {
  xAxis: {
    type: 'category',
    name: '频率',
    nameLocation: 'center',
    nameGap: '30',
    data: ['7.5', '9.75', '10.25', '12.25', '14.25', 'Avg']
  },
  yAxis: {
    type: 'value',
    name: '分数',
    nameRotate: '',
    nameLocation: 'center',
    nameGap: '40'
  },
  series: [
    {
      data: [
        55,
        65,
        45,
        54,
        55,
        {
          value: 55,
          itemStyle: {
            color: '#a90000'
          }
        },
      ],
      type: 'bar'
    }
  ]
};