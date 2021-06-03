import { RadialGauge, LinearGauge } from "canvas-gauges";
import React from "react";

import "./styles.css";

class ReactCanvasGauge extends React.Component {
  componentDidMount() {
    let options = { ...this.props, renderTo: this.canvasRef };

    switch (this.props.gaugeType) {
      case "LINEAR":
        // options.update();
        options = {
          ...this.props,
          renderTo: this.canvasRef,
          width: 400,
          height: 150,
          minValue: 0,
          maxValue: 100,
          majorTicks: ["CALM", "FUMING"],
          minorTicks: 5,
          strokeTicks: true,
          ticksWidth: 15,
          ticksWidthMinor: 7.5,
          // tickSide: "left",
          numberSide: "left",
          // needleSide: "left",
          highlights: [
            {
              from: 0,
              to: 50,
              color: "rgba(0,0, 255, .3)",
            },
            {
              from: 50,
              to: 100,
              color: "rgba(255, 0, 0, .3)",
            },
          ],
          colorMajorTicks: "#aaa",
          colorMinorTicks: "#aaa",
          colorTitle: "#eee",
          colorNumbers: "#eee",
          colorPlate: "#000",
          colorPlateEnd: "#000",
          borderShadowWidth: 0,
          borders: false,
          needleType: "arrow",
          needleWidth: 5,
          animationDuration: 1500,
          animationRule: "linear",
          colorNeedle: "#f5f5f5",
          colorNeedleEnd: "",
          colorBarProgress: "#33ff00",
          colorBar: "#000",
          barStroke: 0,
          barWidth: 8,
          barBeginCircle: false,
        };
        this.gauge = new LinearGauge(options).draw();
        break;
      case "RADIAL":
        options = {
          ...this.props,
          renderTo: this.canvasRef,
          minValue: 0,
          maxValue: 100,
          // minorTicks: 22,
          // ticksAngle: 360,
          startAngle: 45,
          colorPlate: "#000",
          colorMajorTicks: "#f5f5f5",
          colorMinorTicks: "#ddd",
          colorNumbers: "#ccc",
          colorNeedle: "#3f0",
          colorNeedleEnd: "#3f0",
          valueBox: false,
          // colorCircleInner: "#fff",
          colorNeedleCircleOuter: "#ccc",
          needleCircleSize: 15,
          needleCircleOuter: true,
          // animationRule: "linear",
          // needleType: "line",
          needleStart: 5,
          needleEnd: 95,
          // needleWidth: 3,
          borders: true,
          borderInnerWidth: 0,
          borderMiddleWidth: 0,
          borderOuterWidth: 5,
          colorBorderOuter: "#ccc",
          // colorBorderOuterEnd: "#ccc",
          // colorNeedleShadowDown: "#222",
          // borderShadowWidth: 0,
          units: "%",
          // title: "SURVIVAL",
          fontTitleSize: 25,
          // colorTitle: "#f5f5f5",
          animationDuration: 1500,
          highlights: [
            {
              from: 0,
              to: 50,
              color: "rgba(0,0, 255, .3)",
            },
            {
              from: 50,
              to: 100,
              color: "rgba(255, 0, 0, .3)",
            },
          ],
        };
        this.gauge = new RadialGauge(options).draw();
        break;
      default:
        break;
    }
    // this.gauge = new RadialGauge(options).draw();
  }

  componentWillReceiveProps(props) {
    if (this.gauge) {
      console.log(props.value);
      this.gauge.update({ value: props.value });
    }
  }
  render() {
    return <canvas className="gauge" ref={(node) => (this.canvasRef = node)} />;
  }
}

export default ReactCanvasGauge;
