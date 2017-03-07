/*
 * This material is distributed under the GNU General Public License
 * Version 2. You may review the terms of this license at
 * http://www.gnu.org/licenses/gpl-2.0.html
 *
 * Copyright (C) 2001-3 Paul Murrell
 * Copyright (c) 1998-2013, The R Core Team
 * Copyright (c) 2017, Oracle and/or its affiliates
 *
 * All rights reserved.
 */
package com.oracle.truffle.r.library.fastrGrid;

import static com.oracle.truffle.r.library.fastrGrid.Unit.NATIVE;
import static com.oracle.truffle.r.library.fastrGrid.Unit.NPC;
import static com.oracle.truffle.r.library.fastrGrid.Unit.VALID_UNIT_ATTR;
import static com.oracle.truffle.r.nodes.builtin.CastBuilder.Predef.abstractVectorValue;
import static com.oracle.truffle.r.nodes.builtin.CastBuilder.Predef.gte;
import static com.oracle.truffle.r.nodes.builtin.CastBuilder.Predef.lte;
import static com.oracle.truffle.r.nodes.builtin.CastBuilder.Predef.numericValue;

import com.oracle.truffle.api.dsl.Specialization;
import com.oracle.truffle.r.library.fastrGrid.Unit.UnitConversionContext;
import com.oracle.truffle.r.library.fastrGrid.ViewPortContext.VPContextFromVPNode;
import com.oracle.truffle.r.library.fastrGrid.ViewPortTransform.GetViewPortTransformNode;
import com.oracle.truffle.r.library.fastrGrid.device.DrawingContext;
import com.oracle.truffle.r.library.fastrGrid.device.GridDevice;
import com.oracle.truffle.r.nodes.builtin.RExternalBuiltinNode;
import com.oracle.truffle.r.runtime.RInternalError;
import com.oracle.truffle.r.runtime.RRuntime;
import com.oracle.truffle.r.runtime.data.RDataFactory;
import com.oracle.truffle.r.runtime.data.RList;
import com.oracle.truffle.r.runtime.data.model.RAbstractVector;

public abstract class LConvert extends RExternalBuiltinNode.Arg4 {
    @Child private Unit.UnitLengthNode unitLength = Unit.createLengthNode();
    @Child private Unit.UnitToInchesNode unitToInches = Unit.createToInchesNode();
    @Child private GetViewPortTransformNode getViewPortTransform = new GetViewPortTransformNode();
    @Child private VPContextFromVPNode vpContextFromVP = new VPContextFromVPNode();

    static {
        Casts casts = new Casts(LConvert.class);
        casts.arg(0).mustBe(abstractVectorValue());
        casts.arg(1).mustBe(numericValue()).asIntegerVector().findFirst().mustBe(gte(0).and(lte(3)));
        casts.arg(2).mustBe(numericValue()).asIntegerVector().findFirst().mustBe(gte(0).and(lte(3)));
        casts.arg(3).mustBe(numericValue()).asIntegerVector().findFirst().mustBe(gte(0).and(lte(Unit.LAST_NORMAL_UNIT)));
    }

    public static LConvert create() {
        return LConvertNodeGen.create();
    }

    @Specialization
    Object doConvert(RAbstractVector units, int axisFrom, int axisTo, int unitTo) {
        GridContext ctx = GridContext.getContext();
        GridDevice dev = ctx.getCurrentDevice();

        RList currentVP = ctx.getGridState().getViewPort();
        DrawingContext drawingCtx = GPar.asDrawingContext(ctx.getGridState().getGpar());
        ViewPortTransform vpTransform = getViewPortTransform.execute(currentVP);
        ViewPortContext vpContext = vpContextFromVP.execute(currentVP);
        UnitConversionContext conversionCtx = new UnitConversionContext(vpTransform.size, vpContext, drawingCtx);

        int length = unitLength.execute(units);
        double[] result = new double[length];

        int fromUnitId = RRuntime.asInteger(units.getAttr(VALID_UNIT_ATTR));
        boolean relativeUnits = isRelative(unitTo) || isRelative(fromUnitId);
        if ((vpTransform.size.getHeight() < 1e-6 || vpTransform.size.getWidth() < 1e-6) && relativeUnits) {
            throw RInternalError.unimplemented("L_convert: relative units with close to zero width or height");
        }

        for (int i = 0; i < length; i++) {
            double inches;
            if (isXAxis(axisFrom)) {
                inches = unitToInches.convertX(units, i, conversionCtx);
            } else {
                inches = unitToInches.convertY(units, i, conversionCtx);
            }
            if (isXAxis(axisTo)) {
                result[i] = Unit.convertFromInches(inches, unitTo, vpTransform.size.getWidth(), vpContext.xscalemin, vpContext.xscalemax, drawingCtx);
            } else {
                result[i] = Unit.convertFromInches(inches, unitTo, vpTransform.size.getHeight(), vpContext.yscalemin, vpContext.yscalemax, drawingCtx);
            }
        }

        return RDataFactory.createDoubleVector(result, RDataFactory.COMPLETE_VECTOR);
    }

    private static boolean isRelative(int unitId) {
        return unitId == NPC || unitId == NATIVE;
    }

    // what = 0 means x, 1 means y, 2 means width, 3 means height
    private static boolean isXAxis(int what) {
        return what % 2 == 0;
    }
}
