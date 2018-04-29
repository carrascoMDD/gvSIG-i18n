# -*- coding: utf-8 -*-
#
# File: TRAElemento_Constants_Xxx.py
#
# Copyright (c) 2008, 2009, 2010 by Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#
# Authors: 
# Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana (Spain) <gvSIGi18n@gvSIG.org>  
# Model Driven Development sl  Valencia (Spain) <http://www.ModelDD.org> 
# Antonio Carrasco Valero                       <carrasco@ModelDD.org>
#
#
__author__ = """Conselleria de Infraestructuras y Transporte de la Generalidad Valenciana <gvSIGi18n@gvSIG.org>, 
Model Driven Development sl <gvSIGi18n@ModelDD.org>, 
Antonio Carrasco Valero <carrasco@ModelDD.org>"""
__docformat__ = 'plaintext'

from TRAElemento_Constants import cUnderDevelopmentOrDebug


# #######################################
"""Initial value of global to ignore all profiling service requests.

"""
cTRAExecutionProfilingIgnored       = False





# #######################################
"""Names of configuration properties of execution profile capture, rendering and logging. 

"""   
cTRAExecutionProfilingEnablementConfiguration_PropertyNames = [
    'execution_profiling_enabled',
    'execution_timestamping_enabled',
    'execution_auto_root_record_enabled',
    'execution_logging_enabled',
    'execution_logging_detailed_enabled',
    'execution_rendering_enabled',
    'timestamp_rendering_enabled',
]





# #######################################
"""Initial values for configuration of the GLOBAL execution profile capture, rendering and logging. Set to False for production.

"""

if cUnderDevelopmentOrDebug:
    cTRAExecutionProfilingEnabled       = True
    cTRAExecutionTimestampingEnabled    = True
    cTRAExecutionAutoRootRecordEnabled  = True
    cTRAExecutionLoggingEnabled         = True
    cTRAExecutionLoggingDetailedEnabled = True
    cTRAExecutionRenderingEnabled       = True
    cTRATimestampRenderingEnabled       = True
    
    cLogInicializarSimbolosCadenasOrdenados = True
    
else:
    
    cTRAExecutionProfilingEnabled       = False
    cTRAExecutionTimestampingEnabled    = False
    cTRAExecutionAutoRootRecordEnabled  = False
    cTRAExecutionLoggingEnabled         = False
    cTRAExecutionLoggingDetailedEnabled = False
    cTRAExecutionRenderingEnabled       = False
    cTRATimestampRenderingEnabled       = False
    
    cLogInicializarSimbolosCadenasOrdenados = False


    
"""Key for global execution profiling enablement configuration.

"""
cTRAExecutionProfilingEnablementConfiguration_Global    = '::ExecutionProfilingEnablementConfiguration_Global::'






cTimeStampingEnabled             = True
cTimeProfilingEnabled            = True

