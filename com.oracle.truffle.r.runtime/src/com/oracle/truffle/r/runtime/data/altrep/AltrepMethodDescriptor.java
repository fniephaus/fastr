package com.oracle.truffle.r.runtime.data.altrep;

import com.oracle.truffle.r.runtime.ffi.RFFIFactory;

public class AltrepMethodDescriptor {
    public final Object method;
    public final RFFIFactory.Type rffiType;

    public AltrepMethodDescriptor(Object method, RFFIFactory.Type rffiType) {
        this.method = method;
        this.rffiType = rffiType;
    }
}
