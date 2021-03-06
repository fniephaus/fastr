/*
 * Copyright (c) 2015, 2019, Oracle and/or its affiliates. All rights reserved.
 * DO NOT ALTER OR REMOVE COPYRIGHT NOTICES OR THIS FILE HEADER.
 *
 * This code is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License version 3 only, as
 * published by the Free Software Foundation.
 *
 * This code is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License
 * version 3 for more details (a copy is included in the LICENSE file that
 * accompanied this code).
 *
 * You should have received a copy of the GNU General Public License version
 * 3 along with this work; if not, write to the Free Software Foundation,
 * Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA.
 *
 * Please contact Oracle, 500 Oracle Parkway, Redwood Shores, CA 94065 USA
 * or visit www.oracle.com if you need additional information or have any
 * questions.
 */
package com.oracle.truffle.r.nodes.control;

import com.oracle.truffle.api.frame.VirtualFrame;
import com.oracle.truffle.api.nodes.BlockNode;
import com.oracle.truffle.api.nodes.BlockNode.ElementExecutor;
import com.oracle.truffle.api.source.SourceSection;
import com.oracle.truffle.r.nodes.RASTUtils;
import com.oracle.truffle.r.runtime.ArgumentsSignature;
import com.oracle.truffle.r.runtime.nodes.RNode;
import com.oracle.truffle.r.runtime.nodes.RSyntaxLookup;
import com.oracle.truffle.r.runtime.nodes.RSyntaxNode;

final class RBlockNode extends AbstractBlockNode implements ElementExecutor<RNode> {

    private static final int VISIBLE_EXECUTE = 1;
    private static final int NON_VISIBLE_EXECUTE = 0;
    @Child private BlockNode<RNode> blockNode;

    RBlockNode(SourceSection src, RSyntaxLookup operator, RNode[] sequence) {
        super(src, operator);
        blockNode = BlockNode.create(sequence, this);
    }

    public RNode[] getSequence() {
        return blockNode.getElements();
    }

    @Override
    public Object execute(VirtualFrame frame) {
        return blockNode.executeGeneric(frame, NON_VISIBLE_EXECUTE);
    }

    @Override
    public void voidExecute(VirtualFrame frame) {
        blockNode.executeVoid(frame, NON_VISIBLE_EXECUTE);
    }

    @Override
    public Object visibleExecute(VirtualFrame frame) {
        return blockNode.executeGeneric(frame, VISIBLE_EXECUTE);
    }

    @Override
    public RSyntaxNode[] getSyntaxArguments() {
        return RASTUtils.asSyntaxNodes(getSequence());
    }

    @Override
    public ArgumentsSignature getSyntaxSignature() {
        return ArgumentsSignature.empty(getSequence().length);
    }

    // Implementation of the NodeExecutor interface:

    @Override
    public void executeVoid(VirtualFrame frame, RNode node, int index, int argument) {
        node.voidExecute(frame);
    }

    @Override
    public Object executeGeneric(VirtualFrame frame, RNode node, int index, int argument) {
        // executeGeneric is called only for the last node
        assert index == getSequence().length - 1;
        if (argument == VISIBLE_EXECUTE) {
            return node.visibleExecute(frame);
        } else {
            return node.execute(frame);
        }
    }
}
